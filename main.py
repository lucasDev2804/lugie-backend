import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime

# Configuração para salvar as mensagens
MESSAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'messages')
os.makedirs(MESSAGES_DIR, exist_ok=True)

# Define o caminho da pasta static de forma absoluta
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, static_folder=static_dir)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para permitir requisições do frontend
CORS(app)

@app.route('/')
def index():
    """Serve o arquivo index.html da pasta static."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve outros arquivos estáticos (css, js, imagens)."""
    return send_from_directory(app.static_folder, path)

@app.route('/contact', methods=['POST'])
def contact():
    """Endpoint para receber e salvar mensagens do formulário de contato."""
    try:
        data = request.get_json()
        
        # Validação básica
        if not all(key in data for key in ['name', 'email', 'service', 'message']):
            return jsonify({"success": False, "message": "Dados incompletos."}), 400

        # Adiciona timestamp
        data['timestamp'] = datetime.now().isoformat()
        
        # Cria nome do arquivo
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"contact_{timestamp_str}.json"
        filepath = os.path.join(MESSAGES_DIR, filename)
        
        # Salva a mensagem em um arquivo JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        return jsonify({"success": True, "message": "Mensagem recebida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
