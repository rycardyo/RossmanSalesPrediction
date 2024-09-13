import requests 
from flask import Flask, request, Response
import json 


TOKEN = ''
METHOD_NAME = {'UPDATES' : 'geUpdates',
               'SEND'    : 'sendMessage'
               }
chat_id = '918181429'


def model_pipeline(data):
    url = 'http://192.168.100.40:5000/rossmann/predict'
    header = {'Content-type' : 'application/json'}
    #data = json.dumps(df_test_raw.sample(1).to_dict(orient = 'records')) 

    print(data)
    r = requests.post(url, data = data, headers = header)
    print(f'Status Code {r.status_code}')
    print(f'O retorno foi: {r.json()}')
    
    return r.json()

def parse_message(message : dict) -> tuple:
    chat_id  = message['message']['chat']['id']
    store_id = message['message']['text']
    store_id = store_id.replace('/','')

    try:
        store_id = int(store_id)
    
    except ValueError:
        store_id = 'ERROR'


    return chat_id, store_id


def send_message(chat_id : int, 
                 message : str):
    
    CURRENT_METHOD = METHOD_NAME['SEND']
    URL = f'https://api.telegram.org/bot{TOKEN}/{CURRENT_METHOD}?chat_id={chat_id}&text={MESSAGE}'
    
    requests.post(
        URL,
        json = {'text' : message}
    )



app = Flask(__name__)

@app.rourte('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.get_json()

        chat_id, store_id = parse_message(message)
        data = ''

        if store_id != 'ERROR':
            model_prediction = model_pipeline(data)

            return_message = f'A loja {model_prediction['store']} irá vender {model_prediction['sales']} nas próximas 6 semanas'
            
            send_message(return_message)

            return Response('Ok', status = 200)
        
        
        send_message(chat_id, 'ERROR, O ID DA LOJA DEVE SER UM NUMERO')
        
        return Response('Ok', status = 200)
        



