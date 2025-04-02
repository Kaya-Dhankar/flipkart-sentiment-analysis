from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)
    sentiment_type = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    fake_review = db.Column(db.Boolean, nullable=False)
    keywords = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "review_text": self.review_text,
            "sentiment_score": self.sentiment_score,
            "sentiment_type": self.sentiment_type,
            "summary": self.summary,
            "fake_review": self.fake_review,
            "keywords": self.keywords,
        }
