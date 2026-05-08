from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models.participante import db
from routes.inscricao import inscricao_bp
from routes.pagamento import pagamento_bp
from routes.admin import admin_bp
from routes.documentos import documentos_bp
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'acampax-secret-2024')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

app.register_blueprint(inscricao_bp, url_prefix='/api/inscricao')
app.register_blueprint(pagamento_bp, url_prefix='/api/pagamento')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(documentos_bp, url_prefix='/api/documentos')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({'status': 'online', 'projeto': 'Acampax'})

if __name__ == '__main__':
    app.run(debug=True)
