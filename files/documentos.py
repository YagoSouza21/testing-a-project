from flask import Blueprint, request, jsonify, current_app, send_from_directory
from models.participante import db, Participante
from werkzeug.utils import secure_filename
import os

documentos_bp = Blueprint('documentos', __name__)

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'pdf', 'webp'}

def extensao_permitida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS


@documentos_bp.route('/upload/<int:participante_id>', methods=['POST'])
def upload_documento(participante_id):
    p = Participante.query.get_or_404(participante_id)

    if 'frente' not in request.files and 'verso' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    pasta_participante = os.path.join(upload_folder, str(participante_id))
    os.makedirs(pasta_participante, exist_ok=True)

    salvos = []

    if 'frente' in request.files:
        arquivo = request.files['frente']
        if arquivo.filename and extensao_permitida(arquivo.filename):
            nome_seguro = secure_filename(f"frente_{arquivo.filename}")
            caminho = os.path.join(pasta_participante, nome_seguro)
            arquivo.save(caminho)
            p.documento_frente = caminho
            salvos.append('frente')

    if 'verso' in request.files:
        arquivo = request.files['verso']
        if arquivo.filename and extensao_permitida(arquivo.filename):
            nome_seguro = secure_filename(f"verso_{arquivo.filename}")
            caminho = os.path.join(pasta_participante, nome_seguro)
            arquivo.save(caminho)
            p.documento_verso = caminho
            salvos.append('verso')

    if not salvos:
        return jsonify({'erro': 'Nenhum arquivo válido foi enviado. Use PNG, JPG, JPEG, WEBP ou PDF.'}), 400

    db.session.commit()
    return jsonify({'mensagem': 'Documentos enviados com sucesso', 'salvos': salvos})


@documentos_bp.route('/ver/<int:participante_id>/<lado>', methods=['GET'])
def ver_documento(participante_id, lado):
    p = Participante.query.get_or_404(participante_id)

    if lado == 'frente':
        caminho = p.documento_frente
    elif lado == 'verso':
        caminho = p.documento_verso
    else:
        return jsonify({'erro': 'Lado inválido. Use "frente" ou "verso"'}), 400

    if not caminho or not os.path.exists(caminho):
        return jsonify({'erro': 'Documento não encontrado'}), 404

    pasta = os.path.dirname(caminho)
    nome = os.path.basename(caminho)
    return send_from_directory(pasta, nome)


@documentos_bp.route('/status/<int:participante_id>', methods=['GET'])
def status_documentos(participante_id):
    p = Participante.query.get_or_404(participante_id)
    return jsonify({
        'participante_id': p.id,
        'nome': p.nome,
        'documento_frente': bool(p.documento_frente),
        'documento_verso': bool(p.documento_verso),
    })
