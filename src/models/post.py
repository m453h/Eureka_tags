from datetime import datetime
from src import db

post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True),
                             onupdate=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')

    def __repr__(self):
        return f"User('{self.title}', '{self.date_created}')"
