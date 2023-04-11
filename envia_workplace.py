import requests
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# URL to scrape
url = 'https://graph.facebook.com/v4.0/me/messages'

# Token
token=os.getenv('TOKEN')

# Preparando o payload para o POST

# Headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}

def enviarMensagemWorkplace(id: int, msg: str):
    try:
        payload = {
            'message_type': "UPDATE",
            'recipient': {
                'id': id
            },
            'message': {
                'text': msg
            }
        }
        
        r = requests.post(url, headers=headers, json=payload)
        print('Mensagem enviada com sucesso!')
        print(r.status_code)
        print(r.text)
    except Exception as e:
        print('Erro ao enviar mensagem para o usuário: ', e)



       