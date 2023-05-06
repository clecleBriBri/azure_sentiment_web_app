from flask import Flask, render_template, request
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os
import requests
from db import DBSentiment


def authenticate_client():
    key = os.environ.get("AZURE_TEXT_ANALYTICS_KEY")
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
    url = (
        "https://fct-app-jc-review.azurewebsites.net/api/GetComments?code=N8Ttd1qwvB3iEaMhw0eJkkSf4XLmKlikMVPa3nazF5jJAzFuPesVVQ==&name="
        + name
    )
    headers = {"Content-type": "application/json"}
    response = requests.post(url, headers=headers)
    return response.text.replace("[", "").replace("]", "")


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def analyze():
    db_conn = DBSentiment()
    text = request.form["text"]
    text = text.strip().replace(" ", "_").lower()
    if len(db_conn.get_movie(text)) > 0:
        movie_stats_from_db = db_conn.get_movie(text)[0]
        return render_template(
            "index.html",
            movie_name=movie_stats_from_db[0],
            partial_results=movie_stats_from_db[1],
        )
    client = authenticate_client()
    if text == "":
        return render_template("index.html", error="Please enter a name.")

    reviews = getReviews(text)
    if len(reviews) == 0:
        return render_template("index.html", error="No reviews found.")
    # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
    results = sentiment_analysis(client, [reviews])
    db_conn.add_to_db(text, results[0]["sentiment"])
    return render_template("index.html", results=results[0])


if __name__ == "__main__":
    app.run(debug=True)
