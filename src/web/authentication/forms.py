""" Defines a module containing user authentication forms """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
from src import bcrypt
from src.models.user import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    """
    Defines Account Registration Form
    This class inherits from FlaskForm,
    It  has five fields namely:
         full_name: The full name of the user (must have length greater or
                    equal to 3)

        email: E-mail address of the user which is used as the username
                (must be unique)

        password: The password used by the user to login

        confirm_password: This field is used to confirm that the user
                        has entered a correct password during registration

        submit: The form submit button
    """
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
        """
        Defines a method for verifying that the supplied email is unique
        Args:
             email (StringField): The email address to be validated.

        Raises:
            ValidationError: Raised when the provided email address is already
                             registered by another user.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The provided email address is already '
                                  'registered. Please choose a different one')


class LoginForm(FlaskForm):
    """
    Defines Login Form

    It has three fields namely:
        username: The full name of the user (must not be empty, and
        have a proper email format)

        password: The password for the provided username

        submit: The form submit button
    """
    username = StringField('Username',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    """
    Defines Password Reset Request Form

    It has two fields namely:
        email: The email user registered with

        submit: The form submit button
    """
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Reset Password')


class ResetPasswordForm(FlaskForm):
    """
    Defines Reset Password Form

    It has three fields namely:
        password: The new password to use for the account

        confirm_password: Repeat (password) to confirm that the user has
            entered a correct password

        submit: The form submit button
    """
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
    """
    Defines Logged in User Password Change Form

    It has three fields namely:
        current_password: The current password of the logged in user

        password: The new password to use for the account

        confirm_password: Repeat (password) to confirm that the user has
            entered a correct password

        submit: The form submit button
    """
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
        """
        Defines a method for validating the entered current user password
        is correct
        Args:
             field (PasswordField): The password field to verify.

        Raises:
            ValidationError: Raised when the provided password is incorrect.
        """
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Incorrect current password'
                                  ' has been entered')

    def validate_password(self, field):
        """
        Defines a method for ensuring the new entered password is not the same
        as the current user password
        Args:
             field (PasswordField): The password field to verify.

        Raises:
            ValidationError: Raised when the provided password is the same as
                             the current password
        """
        if field.data == self.current_password.data:
            raise ValidationError('New password must be different from the '
                                  'current password.')
