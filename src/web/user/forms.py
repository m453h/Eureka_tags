from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, validators
from wtforms.validators import Length, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from src.models.tag import Tag
from src import db


def tags_choice_query():
    return db.session.query(Tag)


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=10)])
    content = TextAreaField('content')
    is_public = BooleanField('Make this post visible to everyone')
    tags = QuerySelectMultipleField('Select a maximum of (3) tags that best describes your work',
                                    query_factory=tags_choice_query, allow_blank=False,
                                    get_label='name',
                                    validators=[validators.DataRequired()]
                                    )

    submit = SubmitField('Save changes')
