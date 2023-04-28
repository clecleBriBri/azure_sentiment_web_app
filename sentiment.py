from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os

def authenticate_client():
    key = "fbc517233178440e9c97da8d49fbb87a"
    endpoint = "https://cognitive-jc-review.cognitiveservices.azure.com/"
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

def sentiment_analysis(client, documents):
    response = client.analyze_sentiment(documents)
    for idx, doc in enumerate(response):
        print(f"Document {idx+1}:")
        print(f"  Overall sentiment: {doc.sentiment}")
        print("  Sentiment scores:")
        print(f"    Positive: {doc.confidence_scores.positive}")
        print(f"    Neutral: {doc.confidence_scores.neutral}")
        print(f"    Negative: {doc.confidence_scores.negative}\n")

if __name__ == "__main__":
    client = authenticate_client()

    documents = [
        "I am really happy with the new product.",
        "The customer service is terrible.",
        "I love this new feature, it's amazing!"
    ]

    sentiment_analysis(client, documents)
