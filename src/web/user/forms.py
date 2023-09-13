""" Defines a module containing user forms """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, \
    validators
from wtforms.validators import Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from src import db
from src.models.tag import Tag


def tags_choice_query():
    """
        Defines the function that queries for tags in the database

        These tags are used in the QuerySelectMultipleField as the
        query_factory that renders the dropdown list choices.
     """
    return db.session.query(Tag)


class PostForm(FlaskForm):
    """
    Defines Post Creation Form
    This class inherits from FlaskForm,
    It  has five fields namely:
         title: The descriptive name of the post being created

         content: The content (body) of the post being created

        is_public: A flag determining if the post should be visible to everyone

        tags: A list of tags associated with the post

        submit: The form submit button
    """
    title = StringField('Title', validators=[Length(min=10)])
    content = TextAreaField('content')
    is_public = BooleanField('Make this post visible to everyone')
    tags = QuerySelectMultipleField('Select a maximum of (3) tags that best '
                                    'describes your work',
                                    query_factory=tags_choice_query,
                                    allow_blank=False,
                                    get_label='name',
                                    validators=[validators.DataRequired()]
                                    )

    submit = SubmitField('Save changes')
