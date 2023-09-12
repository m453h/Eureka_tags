from sqlalchemy.orm import object_session

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from src import db, login_manager, app
from src.models import post
from datetime import datetime
from flask_login import UserMixin

from src.models.post import Post
from src.models.tag import Tag


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
    has_password_reset_token = db.Column(db.Boolean, nullable=False, default=0)


    @property
    def active_tags(self):
        return object_session(self).query(Tag) \
            .join(Post, Tag.posts) \
            .filter(Post.user_id == self.id) \
            .distinct() \
            .all()

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}', '{self.full_name}', '{self.account_status}')"
