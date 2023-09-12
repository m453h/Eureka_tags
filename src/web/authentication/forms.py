from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError

from src import bcrypt
from src.models.user import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name',
                            validators=[DataRequired(), Length(min=3)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message='Passwords '
                                                                 'must match')
                                                 ])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The provided email address is already '
                                  'registered. Please choose a different one')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message='Passwords'
                                                                 ' must match')
                                                 ])

    submit = SubmitField('Reset Password')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password',
                                     validators=[DataRequired()])

    password = PasswordField('New Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message='Passwords'
                                                                 ' must match')
                                                 ])

    submit = SubmitField('Reset Password')

    def validate_current_password(self, field):
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Incorrect current password'
                                  ' has been entered')

    def validate_password(self, field):
        if field.data == self.current_password.data:
            raise ValidationError('New password must be different from the '
                                  'current password.')
