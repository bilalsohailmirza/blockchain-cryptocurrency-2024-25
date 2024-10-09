# Install necessary packages
!pip install transformers
!pip install torch


# Import modules
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


# Function to load a general-purpose text classification model
def load_classification_model():
    # Using distilbert-base-uncased-finetuned-sst-2-english for simplicity
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model


# Function to detect fake news based on classification (using sentiment model for simplicity)
def detect_fake_news(articles):
    tokenizer, model = load_classification_model()
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)


    results = []
    for article in articles:
        # Get classification
        result = classifier(article, truncation=True)[0]
        label = 'Real' if result['label'] == 'POSITIVE' else 'Fake'
        score = result['score']
        results.append({'article': article, 'label': label, 'score': score})


    return results


# Main function to classify and print results
def classify_articles(articles):
    results = detect_fake_news(articles)
    for i, result in enumerate(results, 1):
        print(f"Article {i}:")
        print(f"Summary: {result['article'][:50]}...")  # Show the first 50 characters for brevity
        print(f"Prediction: {result['label']} (Confidence: {result['score']:.2f})\n")


# Example usage (Replace with your list of articles)
articles = [
    "The stock market has seen an unprecedented rise today due to new policies.",
    "Aliens have landed on Earth and established contact with humans.",
    "Pakistan was founded in 1947 by George Bush."
]
classify_articles(articles)
