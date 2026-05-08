from flask import Blueprint, request, jsonify, current_app
from models.participante import db, Participante
import mercadopago
import os

pagamento_bp = Blueprint('pagamento', __name__)

def get_mp_sdk():
    token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
    if not token:
        raise ValueError('MERCADOPAGO_ACCESS_TOKEN não configurado no .env')
    sdk = mercadopago.SDK(token)
    return sdk


@pagamento_bp.route('/criar/<int:participante_id>', methods=['POST'])
def criar_pagamento(participante_id):
    p = Participante.query.get_or_404(participante_id)

    if p.pagamento_status == 'aprovado':
        return jsonify({'erro': 'Pagamento já aprovado'}), 400

    try:
        sdk = get_mp_sdk()
    except ValueError as e:
        return jsonify({'erro': str(e)}), 500

    valor_total = float(os.getenv('VALOR_INSCRICAO', '150.00'))
    base_url = os.getenv('BASE_URL', 'http://localhost:5000')

    preference_data = {
        "items": [
            {
                "title": f"Inscrição Acampax - {p.nome}",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor_total
            }
        ],
        "payer": {
            "name": p.nome,
            "email": p.email or "sem-email@acampax.com"
        },
        "payment_methods": {
            "excluded_payment_types": [],
            "installments": p.parcelas or 1
        },
        "back_urls": {
            "success": f"{base_url}/api/pagamento/sucesso",
            "failure": f"{base_url}/api/pagamento/falha",
            "pending": f"{base_url}/api/pagamento/pendente"
        },
        "auto_return": "approved",
        "external_reference": str(p.id),
        "notification_url": f"{base_url}/api/pagamento/webhook"
    }

    result = sdk.preference().create(preference_data)
    preference = result.get("response", {})

    if result.get("status") != 201:
        return jsonify({'erro': 'Erro ao criar preferência de pagamento', 'detalhe': preference}), 500

    p.mercadopago_preference_id = preference.get("id")
    db.session.commit()

    return jsonify({
        'preference_id': preference.get("id"),
        'init_point': preference.get("init_point"),
        'sandbox_init_point': preference.get("sandbox_init_point")
    })


@pagamento_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json() or {}
    topic = data.get('type') or request.args.get('topic')
    resource_id = data.get('data', {}).get('id') or request.args.get('id')

    if topic not in ('payment', 'merchant_order'):
        return jsonify({'status': 'ignorado'}), 200

    try:
        sdk = get_mp_sdk()
    except ValueError:
        return jsonify({'erro': 'SDK não configurado'}), 500

    if topic == 'payment' and resource_id:
        result = sdk.payment().get(resource_id)
        payment = result.get("response", {})

        external_ref = payment.get("external_reference")
        status = payment.get("status")

        if external_ref:
            p = Participante.query.get(int(external_ref))
            if p:
                p.mercadopago_id = str(resource_id)
                if status == 'approved':
                    p.pagamento_status = 'aprovado'
                elif status == 'rejected':
                    p.pagamento_status = 'rejeitado'
                elif status == 'pending':
                    p.pagamento_status = 'pendente'
                db.session.commit()

    return jsonify({'status': 'ok'}), 200


@pagamento_bp.route('/sucesso', methods=['GET'])
def sucesso():
    payment_id = request.args.get('payment_id')
    external_ref = request.args.get('external_reference')

    if external_ref:
        p = Participante.query.get(int(external_ref))
        if p:
            p.pagamento_status = 'aprovado'
            p.mercadopago_id = payment_id
            db.session.commit()

    return jsonify({'mensagem': 'Pagamento aprovado!', 'participante_id': external_ref})


@pagamento_bp.route('/falha', methods=['GET'])
def falha():
    return jsonify({'mensagem': 'Pagamento falhou. Tente novamente.'})


@pagamento_bp.route('/pendente', methods=['GET'])
def pendente():
    return jsonify({'mensagem': 'Pagamento pendente. Aguardando confirmação.'})


@pagamento_bp.route('/status/<int:participante_id>', methods=['GET'])
def status_pagamento(participante_id):
    p = Participante.query.get_or_404(participante_id)
    return jsonify({
        'participante_id': p.id,
        'nome': p.nome,
        'pagamento_status': p.pagamento_status,
        'mercadopago_id': p.mercadopago_id
    })
