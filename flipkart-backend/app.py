from flask import Flask, request, jsonify
from textblob import TextBlob
from langdetect import detect
from deep_translator import GoogleTranslator
import nltk
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Ensure necessary NLTK corpora are downloaded
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

# Load the dataset
file_path = "flipkart_data.csv"
data = pd.read_csv(file_path)

# Sentiment Analysis Function
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    return "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"

# Rating Calculation Function
def calculate_rating(sentiment):
    if sentiment == "positive":
        return 4 + round((TextBlob(sentiment).sentiment.polarity) * 1)  # Rating between 4 and 5
    elif sentiment == "neutral":
        return 3  # Neutral sentiment gets an average rating
    else:
        return 1 + round((TextBlob(sentiment).sentiment.polarity) * 1)  # Rating between 1 and 2

# Keyword Extraction Function
def extract_keywords(text):
    words = nltk.word_tokenize(text)
    tagged_words = nltk.pos_tag(words)
    keywords = [word for word, tag in tagged_words if tag.startswith("NN")]
    return keywords

# Fake Review Detection Function
def detect_fake_review(text):
    words = text.lower().split()
    word_count = len(words)
    unique_words = len(set(words))
    return "possible fake" if unique_words / word_count < 0.5 else "genuine"

# Language Detection and Translation Function
def detect_language_and_translate(text):
    try:
        lang = detect(text)
        translated_text = (
            GoogleTranslator(source=lang, target="en").translate(text)
            if lang != "en"
            else text
        )
        return lang, translated_text
    except:
        return "unknown", text

# Home Route
@app.route("/")
def home():
    return "<h2>Welcome to Flipkart Reviews Sentiment Analysis API!</h2>"

# Get All Reviews Endpoint
@app.route("/reviews", methods=["GET"])
def get_reviews():
    try:
        reviews = data.to_dict(orient="records")

        for review in reviews:
            review["sentiment"] = analyze_sentiment(review["review"])
            review["rating"] = calculate_rating(review["sentiment"])
            review["keywords"] = extract_keywords(review["review"])
            review["fake"] = detect_fake_review(review["review"])
            review["language"], review["translation"] = detect_language_and_translate(
                review["review"]
            )

        return jsonify(reviews)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add Review Endpoint
@app.route("/reviews", methods=["POST"])
def add_review():
    try:
        req_data = request.get_json()
        new_review_text = req_data.get("content", "")

        if not new_review_text.strip():
            return jsonify({"error": "Review content cannot be empty"}), 400

        sentiment = analyze_sentiment(new_review_text)
        rating = calculate_rating(sentiment)

        new_review = {
            "review": new_review_text,
            "rating": rating,
            "sentiment": sentiment,
            "keywords": extract_keywords(new_review_text),
            "fake": detect_fake_review(new_review_text),
            "language": detect_language_and_translate(new_review_text)[0],
            "translation": detect_language_and_translate(new_review_text)[1],
        }

        # Append the new review to the DataFrame
        data.loc[len(data)] = new_review
        return jsonify(new_review)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
