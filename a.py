from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get_verification_link', methods=['POST'])
def get_verification_link():
    data = request.json
    email = data['email']
    password = data['password']
    api_key = data['api_key']

    try:
        response = requests.get(
            f'https://api.firstmail.ltd/v1/market/get/message?username={email}&password={password}',
            headers={
                'accept': 'application/json',
                'X-API-KEY': api_key
            }
        )
        response.raise_for_status()
        
        # Acessando a mensagem do email
        message = response.json()['data'][0]['message']
        
        # Carregar o HTML da mensagem com BeautifulSoup
        soup = BeautifulSoup(message, 'html.parser')
        
        # Extrair o link de verificação do e-mail
        verification_link = None
        for a in soup.find_all('a', href=True):
            if 'verification_email_token' in a['href']:
                verification_link = a['href']
                break
        
        return jsonify({'verification_link': verification_link})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
