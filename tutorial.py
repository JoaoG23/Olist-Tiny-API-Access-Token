import base64
from flask import Flask, redirect, request
import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
# Credenciais da aplicação no Tiny
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# URL de redirecionamento (deve corresponder à configurada no Tiny)
REDIRECT_URI = 'https://0994-2804-2164-1076-9600-d5af-911d-31f9-eb15.ngrok-free.app/oauth/tiny'
@app.route('/', methods=['GET'])
def auth_tiny():
    # Gera um estado aleatório para proteção contra CSRF    
    # Parâmetros para a URL de autorização

    # Redireciona o usuário para a página de autorização do tiny
    # https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth?response_type=code&client_id=tiny-api-256ea7179659f2bb28366b5995c1acedaa6493dd-1743451059&redirect_uri=https%3A%2F%2F0994-2804-2164-1076-9600-d5af-911d-31f9-eb15.ngrok-free.app%2Foauth%2Ftiny    
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI
    }

    AUTHORIZATION_URL = 'https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth'
    redirect_url = f'{AUTHORIZATION_URL}?{urlencode(params)}' 

    return redirect(redirect_url)

@app.route('/oauth/tiny', methods=['GET'])
def oauth_callback():
   
    code = request.args.get('code')
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f"Basic {auth_header}",
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    TOKEN_URL = "https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/token"
    # Faz a requisição para obter o token de acesso
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    token_data = response.json()
    print(token_data)
    access_token = token_data['access_token']
    print('TINY (ACCESS TOKEN): ', access_token)

    return f"Token de acesso: {access_token}", 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)