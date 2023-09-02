from src import db, login_manager
from src.models import post
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(130), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    account_status = db.Column(db.String(2), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.full_name}', '{self.account_status}')"
