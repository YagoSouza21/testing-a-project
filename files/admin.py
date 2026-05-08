from flask import Blueprint, request, jsonify, send_file
from models.participante import db, Participante
from utils.pdf_generator import gerar_autorizacao_pdf
import io

admin_bp = Blueprint('admin', __name__)

# Proteção simples por token — troque no .env
import os
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', 'acampax-admin-2024')

def verificar_token():
    token = request.headers.get('X-Admin-Token') or request.args.get('token')
    return token == ADMIN_TOKEN


@admin_bp.route('/participantes', methods=['GET'])
def listar_participantes():
    if not verificar_token():
        return jsonify({'erro': 'Não autorizado'}), 401

    status_filtro = request.args.get('status')
    menor_filtro = request.args.get('menor')

    query = Participante.query

    if status_filtro:
        query = query.filter_by(pagamento_status=status_filtro)

    if menor_filtro is not None:
        query = query.filter_by(menor_idade=(menor_filtro.lower() == 'true'))

    participantes = query.order_by(Participante.criado_em.desc()).all()

    return jsonify({
        'total': len(participantes),
        'participantes': [p.to_dict() for p in participantes]
    })


@admin_bp.route('/stats', methods=['GET'])
def estatisticas():
    if not verificar_token():
        return jsonify({'erro': 'Não autorizado'}), 401

    total = Participante.query.count()
    aprovados = Participante.query.filter_by(pagamento_status='aprovado').count()
    pendentes = Participante.query.filter_by(pagamento_status='pendente').count()
    rejeitados = Participante.query.filter_by(pagamento_status='rejeitado').count()
    menores = Participante.query.filter_by(menor_idade=True).count()
    autorizacoes = Participante.query.filter_by(autorizacao_entregue=True).count()

    valor = float(os.getenv('VALOR_INSCRICAO', '150.00'))

    return jsonify({
        'total_inscritos': total,
        'pagamentos_aprovados': aprovados,
        'pagamentos_pendentes': pendentes,
        'pagamentos_rejeitados': rejeitados,
        'menores_de_idade': menores,
        'autorizacoes_entregues': autorizacoes,
        'receita_total': aprovados * valor
    })


@admin_bp.route('/autorizacao_entregue/<int:id>', methods=['PUT'])
def marcar_autorizacao(id):
    if not verificar_token():
        return jsonify({'erro': 'Não autorizado'}), 401

    p = Participante.query.get_or_404(id)
    p.autorizacao_entregue = True
    db.session.commit()
    return jsonify({'mensagem': f'Autorização de {p.nome} marcada como entregue'})


@admin_bp.route('/gerar_pdf/<int:id>', methods=['GET'])
def gerar_pdf(id):
    if not verificar_token():
        return jsonify({'erro': 'Não autorizado'}), 401

    p = Participante.query.get_or_404(id)

    if not p.menor_idade:
        return jsonify({'erro': 'Este participante não é menor de idade'}), 400

    pdf_bytes = gerar_autorizacao_pdf(p)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'autorizacao_{p.nome.replace(" ", "_")}.pdf'
    )


import os
