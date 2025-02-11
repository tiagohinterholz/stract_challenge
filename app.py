from flask import Flask, request, jsonify
import requests, json

app = Flask(__name__)

# Configurações External API

BASE_URL = 'https://sidebar.stract.to/api'
HEADERS = {'Authorization': 'ProcessoSeletivoStract2025'}

# rota raiz com dados pessoais
@app.route('/', methods = ['GET'])
def home():
    return jsonify({
        'nome': 'Tiago Francisco Hinterholz',
        'e-mail': 'fh.tiago@gmail.com',
        'linkedin_profile': 'https://www.linkedin.com/in/tiago-hinterholz/'
    })
    
# Obter lista de plataformas external API
@app.route('/platforms', methods = ['GET'])
def get_platforms():
    response = requests.get(f'{BASE_URL}/platforms', headers = HEADERS)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return jsonify(response.json())
    return jsonify({'error': 'Falha no acesso das plataformas'}), response.status_code

# obter as contas de uma plataforma específica
@app.route('/accounts/<platform>', methods = ['GET'])
def get_accounts(platform):
    
    platform_mapping = {
        "facebook": "meta_ads",
        "google": "ga4",
        "tiktok": "tiktok_insights"
    }
    platform_value = platform_mapping.get(platform.lower()) # só garantir a normalização da entrada pra evitar erros
    
    if not platform_value:
        return jsonify({"error": "Plataforma inválida. Use: facebook, google ou tiktok."}), 400

    page = request.args.get("page", 1)
    
    response = requests.get(f'{BASE_URL}/accounts?platform={platform_value}&page={page}', headers = HEADERS)
    
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return jsonify(response.json())
    
    return jsonify({'error': f'Falha no acesso das contas da plataforma {platform}'}), response.status_code

if __name__ == '__main__':
    app.run(debug = True)