from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     # Récupérer les données de la page web
#     movie_title = request.form['movie_title']
    
#     # Envoyer les données à l'API Azure Text Analytics pour analyse de sentiment
#     subscription_key = 'fbc517233178440e9c97da8d49fbb87a'
#     endpoint = 'https://cognitive-jc-review.cognitiveservices.azure.com/'
#     text_analytics_url = endpoint + '/text/analytics/v3.0/sentiment'
#     headers = {'Ocp-Apim-Subscription-Key': subscription_key}
#     data = {'documents': [{'id': '1', 'text': movie_title}]}
#     response = requests.post(text_analytics_url, headers=headers, json=data)
#     sentiment = json.loads(response.text)['documents'][0]['sentiment']

#     # Renvoyer les résultats à la page web
#     return render_template('index.html', sentiment=sentiment)

if __name__ == '__main__':
    app.run()
