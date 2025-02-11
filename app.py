from flask import Flask, request, jsonify
import requests

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
        return jsonify(response.json())
    return jsonify({'error': 'Falha no acesso das plataformas'}), response.status_code

# obter as contas de uma plataforma específica
@app.route('/platform/<platform>', methods = ['GET'])
def get_platform(platform):
    response = requests.get(f'{BASE_URL}/accounts?platforms={platform}', headers = HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({'error': f'Falha no acesso das contas da plataforma {platform}'}), response.status_code

if __name__ == '__main__':
    app.run(debug = True)