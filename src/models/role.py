from datetime import datetime
from src import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)
    users = db.relationship('User', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}')"
