""" Defines a module containing administrator forms """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Length, Email


class TagForm(FlaskForm):
    """
    Defines Tag Form
    This class inherits from FlaskForm, It  has two fields namely:
        name: The descriptive name of the tag being created

        submit: The form submit button
    """
    name = StringField('Name', validators=[validators.DataRequired()])
    submit = SubmitField('Save changes')


class UserForm(FlaskForm):
    """
    Defines User Form
    It  has three fields namely:
        full_name: The name of the full name of the user being edited

        email: The email of the user account being edited

        submit: The form submit button
    """
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=3)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Save Changes')
