from flask import Flask, render_template, request
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os
import requests


def authenticate_client():
    key = os.environ["AZURE_TEXT_ANALYTICS_KEY"]
    endpoint = "https://cognitive-jc-review.cognitiveservices.azure.com/"
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client


def sentiment_analysis(client, documents):
    response = client.analyze_sentiment(documents)
    results = []
    for idx, doc in enumerate(response):
        result = {}
        result["text"] = documents[idx]
        result["sentiment"] = doc.sentiment
        result["positive"] = doc.confidence_scores.positive
        result["neutral"] = doc.confidence_scores.neutral
        result["negative"] = doc.confidence_scores.negative
        results.append(result)
    return results


def getReviews(name: str):
    url = "https://fct-app-jc-review.azurewebsites.net/api/GetComments?code=N8Ttd1qwvB3iEaMhw0eJkkSf4XLmKlikMVPa3nazF5jJAzFuPesVVQ==&name=m3gan"
    headers = {"Content-type": "application/json"}
    response = requests.post(url, headers=headers)
    reviews = response.text
    return reviews


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def analyze():
    client = authenticate_client()
    text = request.form["text"]
    documents = [text]
    reviews = getReviews(documents)
    # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
    reviews = [item for sublist in reviews for item in sublist]
    results = sentiment_analysis(client, reviews)
    return render_template("index.html", results=reviews)


if __name__ == "__main__":
    app.run(debug=True)
