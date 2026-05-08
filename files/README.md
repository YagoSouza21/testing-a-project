# Acampax 🏕️

Sistema completo de inscrições para acampamento com pagamento, upload de documentos, autorização de menores e painel admin.

## Stack
- **Backend**: Flask + SQLAlchemy (SQLite)
- **Pagamento**: Mercado Pago
- **PDF**: ReportLab
- **Frontend**: HTML/CSS/JS puro

---

## Estrutura do projeto

```
acampax/
├── app.py                  # App Flask principal
├── requirements.txt
├── .env.example            # Variáveis de ambiente (copie para .env)
├── models/
│   └── participante.py     # Model do banco de dados
├── routes/
│   ├── inscricao.py        # CRUD de inscrições
│   ├── pagamento.py        # Integração Mercado Pago + webhook
│   ├── admin.py            # Painel admin + geração de PDF
│   └── documentos.py       # Upload de documentos
├── utils/
│   └── pdf_generator.py    # Geração de autorização para menores
├── uploads/                # Documentos enviados (criado automaticamente)
├── index.html              # Landing page
├── inscricao.html          # Formulário de inscrição (4 etapas)
├── admin.html              # Painel administrativo
└── script.js               # JS do botão WhatsApp/Chatbot
```

---

## Como rodar

### 1. Clone e instale
```bash
pip install -r requirements.txt
```

### 2. Configure o .env
```bash
cp .env.example .env
# Edite .env com seu token do Mercado Pago e demais configurações
```

### 3. Inicie o servidor
```bash
python app.py
```

O servidor sobe em `http://localhost:5000`.

### 4. Abra o frontend
Abra `index.html` no navegador (ou sirva com um servidor estático).

---

## Endpoints da API

### Inscrição
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/inscricao/` | Criar inscrição |
| GET | `/api/inscricao/<id>` | Buscar inscrição |
| PUT | `/api/inscricao/<id>` | Atualizar inscrição |
| DELETE | `/api/inscricao/<id>` | Deletar inscrição |

### Pagamento
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/pagamento/criar/<id>` | Criar preferência MP |
| POST | `/api/pagamento/webhook` | Webhook Mercado Pago |
| GET | `/api/pagamento/status/<id>` | Status do pagamento |

### Documentos
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/documentos/upload/<id>` | Upload frente/verso |
| GET | `/api/documentos/ver/<id>/<frente\|verso>` | Visualizar documento |

### Admin (requer `X-Admin-Token` no header)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/admin/participantes` | Listar todos |
| GET | `/api/admin/stats` | Estatísticas gerais |
| PUT | `/api/admin/autorizacao_entregue/<id>` | Marcar autorização |
| GET | `/api/admin/gerar_pdf/<id>` | Baixar PDF de autorização |

---

## Configuração do Mercado Pago

1. Acesse https://www.mercadopago.com.br/developers
2. Crie uma aplicação e obtenha seu **Access Token**
3. Configure `MERCADOPAGO_ACCESS_TOKEN` no `.env`
4. Para testes, use o token de **sandbox** (começa com `TEST-`)
5. Configure a URL do webhook no painel do MP: `https://sua-url.com/api/pagamento/webhook`

## Configuração do Typebot (chatbot)
Em `script.js`, troque a URL do `window.open(...)` pelo link do seu bot no Typebot.
