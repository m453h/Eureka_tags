from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class TagForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    submit = SubmitField('Save changes')
