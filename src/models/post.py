from src import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    is_public = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_created}')"
