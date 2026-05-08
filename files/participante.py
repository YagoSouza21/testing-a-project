from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Participante(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200))
    idade = db.Column(db.Integer, nullable=False)
    cidade = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

    documento_frente = db.Column(db.String(300))
    documento_verso = db.Column(db.String(300))

    menor_idade = db.Column(db.Boolean, default=False)

    responsavel_nome = db.Column(db.String(200))
    responsavel_rg = db.Column(db.String(50))
    responsavel_telefone = db.Column(db.String(20))

    lgpd_aceito = db.Column(db.Boolean, default=False)

    pagamento_status = db.Column(db.String(50), default='pendente')
    forma_pagamento = db.Column(db.String(50))
    parcelas = db.Column(db.Integer, default=1)
    mercadopago_id = db.Column(db.String(100))
    mercadopago_preference_id = db.Column(db.String(200))

    autorizacao_entregue = db.Column(db.Boolean, default=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'idade': self.idade,
            'cidade': self.cidade,
            'telefone': self.telefone,
            'menor_idade': self.menor_idade,
            'responsavel_nome': self.responsavel_nome,
            'responsavel_rg': self.responsavel_rg,
            'responsavel_telefone': self.responsavel_telefone,
            'lgpd_aceito': self.lgpd_aceito,
            'pagamento_status': self.pagamento_status,
            'forma_pagamento': self.forma_pagamento,
            'parcelas': self.parcelas,
            'mercadopago_id': self.mercadopago_id,
            'autorizacao_entregue': self.autorizacao_entregue,
            'documento_frente': bool(self.documento_frente),
            'documento_verso': bool(self.documento_verso),
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }
