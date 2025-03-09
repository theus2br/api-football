from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import requests
from datetime import datetime, timedelta
from collections import Counter

app = Flask(__name__)

## funcao para chamar a API
def api_football(id1, id2):

    url = 'https://v3.football.api-sports.io/fixtures/headtohead'

    headers = {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': 'c71bb04ba5fcde0f4472c79fdc30a088'
    }

    params = {
        'h2h': f'{id1}-{id2}',
        'from': '2020-01-01',
        'to': datetime.strftime(datetime.now(),'%Y-%m-%d')
    }

    return requests.get(url, headers=headers, params=params).json()

## funcao que identifica o ganhador de cada confronto
def identifica_ganhador(confronto):
    if confronto['home']['winner']:
        return confronto['home']['name']
    elif confronto['away']['winner']:
        return confronto['away']['name']
    else:
        return 'Empate'

## exemplo de rota para caso queira retornar uma pagina html
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download-csv")
def download_csv():
    return send_from_directory('temp', 'dados.csv')

@app.route("/head-to-head")
def head_to_head():
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    response = api_football(id1, id2)

    ## criando o dataframe e formatando as features
    df = pd.DataFrame(response['response'])
    df['vencedor'] = df['teams'].apply(identifica_ganhador)
    df['liga'] = df['league'].apply(lambda x: x['name'])
    df['rodada'] = df['league'].apply(lambda x: x['round'])
    df['data'] = df['fixture'].apply(lambda x: (datetime.fromisoformat(x['date']) - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M"))
    df['arbitro'] = df['fixture'].apply(lambda x: x['referee'])
    df['mando_de_campo'] = df['teams'].apply(lambda x: x['home']['name'])
    df['placar'] = df['goals'].apply(lambda x: f"{x['home']}x{x['away']}")
    
    df = df[['data','liga','rodada','arbitro','mando_de_campo','vencedor','placar']]

    df.to_csv('dados.csv', index=False)
    
    ## retornando o dataframe no formato JSON, como exemplo de utilizacao
    return jsonify(df.to_json())

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)