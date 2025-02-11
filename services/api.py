import requests

BASE_URL = 'https://sidebar.stract.to/api'
HEADERS = {'Authorization': 'ProcessoSeletivoStract2025'}

def fetch_data(endpoint, params=None):
    """Faz uma requisição GET para a API externa."""
    url = f'{BASE_URL}/{endpoint}'
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.json()
    
    return {'error': f'Falha ao obter dados de {endpoint}'}, response.status_code
