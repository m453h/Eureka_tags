from src import db
from datetime import datetime


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Tag('{self.id}', '{self.name}')"
