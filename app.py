from flask import Flask, render_template, request
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os
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


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def analyze():
    client = authenticate_client()
    text = request.form["text"]
    documents = [text]
    results = sentiment_analysis(client, documents)
    return render_template("index.html", results=results)



if __name__ == '__main__':
    app.run(debug=True)
