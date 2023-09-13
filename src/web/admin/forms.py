from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Length, Email


class TagForm(FlaskForm):
    """
    Defines Tag Form
    """
    name = StringField('Name', validators=[validators.DataRequired()])
    submit = SubmitField('Save changes')


class UserForm(FlaskForm):
    """
    Defines User Form
    """
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=3)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Save Changes')
