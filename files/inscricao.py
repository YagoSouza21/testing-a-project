from flask import Blueprint, request, jsonify
from models.participante import db, Participante

inscricao_bp = Blueprint('inscricao', __name__)

@inscricao_bp.route('/', methods=['POST'])
def criar_inscricao():
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'Dados inválidos'}), 400

    nome = data.get('nome', '').strip()
    idade = data.get('idade')
    lgpd_aceito = data.get('lgpd_aceito', False)

    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    if not idade:
        return jsonify({'erro': 'Idade é obrigatória'}), 400
    if not lgpd_aceito:
        return jsonify({'erro': 'É necessário aceitar a LGPD'}), 400

    try:
        idade = int(idade)
    except (ValueError, TypeError):
        return jsonify({'erro': 'Idade inválida'}), 400

    menor_idade = idade < 18

    if menor_idade:
        if not data.get('responsavel_nome'):
            return jsonify({'erro': 'Dados do responsável são obrigatórios para menores'}), 400
        if not data.get('responsavel_rg'):
            return jsonify({'erro': 'RG do responsável é obrigatório'}), 400

    participante = Participante(
        nome=nome,
        email=data.get('email', '').strip(),
        idade=idade,
        cidade=data.get('cidade', '').strip(),
        telefone=data.get('telefone', '').strip(),
        menor_idade=menor_idade,
        responsavel_nome=data.get('responsavel_nome', '').strip() if menor_idade else None,
        responsavel_rg=data.get('responsavel_rg', '').strip() if menor_idade else None,
        responsavel_telefone=data.get('responsavel_telefone', '').strip() if menor_idade else None,
        lgpd_aceito=lgpd_aceito,
        forma_pagamento=data.get('forma_pagamento', 'pix'),
        parcelas=int(data.get('parcelas', 1)),
    )

    db.session.add(participante)
    db.session.commit()

    return jsonify({
        'mensagem': 'Inscrição criada com sucesso',
        'id': participante.id,
        'menor_idade': menor_idade
    }), 201


@inscricao_bp.route('/<int:id>', methods=['GET'])
def buscar_inscricao(id):
    p = Participante.query.get_or_404(id)
    return jsonify(p.to_dict())


@inscricao_bp.route('/<int:id>', methods=['PUT'])
def atualizar_inscricao(id):
    p = Participante.query.get_or_404(id)
    data = request.get_json()

    campos = ['nome', 'email', 'cidade', 'telefone', 'responsavel_nome',
              'responsavel_rg', 'responsavel_telefone', 'forma_pagamento', 'parcelas']

    for campo in campos:
        if campo in data:
            setattr(p, campo, data[campo])

    db.session.commit()
    return jsonify({'mensagem': 'Atualizado com sucesso', 'participante': p.to_dict()})


@inscricao_bp.route('/<int:id>', methods=['DELETE'])
def deletar_inscricao(id):
    p = Participante.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'mensagem': 'Inscrição removida'})
