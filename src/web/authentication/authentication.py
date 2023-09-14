#!/usr/bin/python3
""" Defines a module for authentication of user accounts """
import os

from flask import render_template, Blueprint, flash, redirect, url_for
from src.models.user import User
from src import db, bcrypt, login_manager, mail, app
from src.web.authentication.forms import RegistrationForm, LoginForm, \
    RequestResetForm, ResetPasswordForm, \
    ChangePasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

authentication_pages = Blueprint('authentication_pages', __name__,
                                 template_folder='templates')

# Get the configured site domain name
domain_name = os.environ.get('DOMAIN_NAME')


def send_reset_email(user):
    """
    Defines a method for sending password reset e-mail

    Args:
         user (User): The user object used for e-mail operations.
    """
    # Generate a unique token used to authenticate user when resetting their
    # password
    token = user.get_reset_token()

    # Construct the email message object
    msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    reset_link = domain_name + url_for('authentication_pages.reset_token',
                                       token=token)
    # Define the e-mail message body
    html_body = render_template('authentication/password_reset_email.html',
                                recipient_name=user.full_name,
                                reset_link=reset_link
                                )
    msg.html = html_body

    # Send the e-mail
    mail.send(msg)


def send_activation_email(user):
    """
    Defines a method for sending account activation e-mail

    Args:
         user (User): The user object used for e-mail operations.
    """
    # Generate a unique token used to authenticate user when activating their
    # account
    token = user.get_reset_token()

    # Construct the email message object
    msg = Message('Account Activation', sender=app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    activation_link = domain_name + url_for('authentication_pages'
                                            '.activation_token',
                                            token=token)
    # Construct the message body
    html_body = render_template('authentication/activation_email.html',
                                recipient_name=user.full_name,
                                activation_link=activation_link)
    msg.html = html_body

    # Send the e-mail
    mail.send(msg)


@authentication_pages.route('/login', strict_slashes=False,
                            methods=['GET', 'POST'])
def login():
    """ Defines the method for user login operations"""
    # Check if the current user is authenticated, then don't render the
    # login page instead redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    # User is not logged in then create the login form
    form = LoginForm()

    # Check if the form contains valid data
    if form.validate_on_submit():
        # Fetch the user that matches the supplied username (email)
        user = User.query.filter_by(email=form.username.data).first()

        # Check if the hash of the supplied password matches the hash of the
        # stored password
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            # If the password entered is correct then check if the account is
            # active and login the user else, add a flash message to display
            # an error message and redirect the user to the login page
            if user.account_status == "A":
                login_user(user)
            else:
                flash('You need to activate your account before you login',
                      'danger')
            return redirect(url_for('authentication_pages.login'))
        else:
            # If the username or password is not valid then add a flash message
            # and just render the login form
            flash('Invalid username or password', 'danger')

    # Render the login form
    return render_template('authentication/login.html', form=form)


@authentication_pages.route('/register', strict_slashes=False,
                            methods=['GET', 'POST'])
def register():
    """ Defines the method for account registration operations"""

    # Check if the current user is authenticated, then don't render the
    # login page instead redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    # Create the registration form
    form = RegistrationForm()

    # Check if the submitted form has valid data
    if form.validate_on_submit():
        # Hash the current password using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data) \
            .decode('utf-8')
        # Create the instance of the user account
        user = User(email=form.email.data,
                    full_name=form.full_name.data,
                    account_status="I",
                    role_id="1",
                    password=hashed_password)

        # Add the user to the database and commit the changes
        db.session.add(user)
        db.session.commit()

        # Send an e-mail with account activation details
        send_activation_email(user)

        # Add a flash message to notify the user to check their e-mail and
        # redirect the user to the login page
        flash('You are account has been created, please check your e-mail '
              'for your account activation instructions',
              'success')
        return redirect(url_for('authentication_pages.login'))

    # Render the registration form
    return render_template('authentication/register.html', form=form)


@authentication_pages.route('/reset-password', strict_slashes=False,
                            methods=['GET', 'POST'])
def reset_request():
    """ Defines the method for user password reset request """

    # Check if the current user is authenticated, then don't render the
    # page instead redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user.has_password_reset_token = True
        db.session.commit()
        send_reset_email(user)
        flash('An email has been sent with instructions to '
              'reset your password',
              'info')
        return redirect(url_for('authentication_pages.login'))

    return render_template('authentication/password_reset_request.html',
                           form=form)


@authentication_pages.route('/reset-password/<token>', strict_slashes=False,
                            methods=['GET', 'POST'])
def reset_token(token):
    """
    Defines the method for resetting user password based on supplied token

    Args:
        token (string): The token used to authenticate the user
    """
    # Check if the current user is authenticated, then don't render the
    # page instead redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    # Verify token supplied by the user
    user = User.verify_reset_token(token)

    # If the token is not valid or the user has not requested for the token
    # then add a flash message displaying an error and redirect the user to the
    # password reset request page.
    if user is None or not user.has_password_reset_token:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('authentication_pages.reset_request'))

    # Render the password reset form
    form = ResetPasswordForm()

    # If the form is valid then proceed with password reset actions
    if form.validate_on_submit():
        # Hash the new supplied password
        hashed_password = bcrypt.generate_password_hash(form.password.data) \
            .decode('utf-8')

        # Update the user password and reset the password request status
        user.password = hashed_password
        user.has_password_reset_token = False
        db.session.commit()  # Commit changes to the database

        # Add a flash message for successful password reset
        # and redirect the user to the login page
        flash('Your password has been updated, You are now able to log in!',
              'success')
        return redirect(url_for('authentication_pages.login'))

    # Render the password reset form
    return render_template('authentication/password_reset_token.html',
                           form=form)


@authentication_pages.route('/activate/<token>', strict_slashes=False,
                            methods=['GET', 'POST'])
def activation_token(token):
    """
    Defines the method for activating a user account based on a supplied token

    Args:
        token (string): The token used to authenticate the user
    """

    # Check if the current user is authenticated, then don't render the
    # page instead redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    # Verify the user token supplied
    user = User.verify_reset_token(token)

    # If the user token is not valid or the user account is not inactive
    # then add a flash message and redirect the user to the password reset
    # request page
    if user is None or not user.account_status == "I":
        flash('That is an invalid or expired token, please reset'
              ' your password', 'warning')
        return redirect(url_for('authentication_pages.reset_request'))

    # Update the user account status and commit the changes to the database
    user.account_status = 'A'
    db.session.commit()

    # Add a flash message for the successful completion of activation and
    # redirect the user to the login page
    flash('Your account has been successfully activated, You are now able to '
          'log in!', 'success')
    return redirect(url_for('authentication_pages.login'))


@authentication_pages.route('/change-password', strict_slashes=False,
                            methods=['GET', 'POST'])
@login_required
def change_password():
    """ Defines the method for changing password of logged in user(s) """

    # Create the Change Password form
    form = ChangePasswordForm()

    # Check if the Change Password form is valid
    if form.validate_on_submit():
        # Set the current user's password hash to the hash of the supplied
        # new password and commit the changes to the database
        current_user.password = bcrypt \
            .generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()

        # Add a flash message for the successful completion of password change,
        # logout the user and redirect the user to the login page
        flash('Your password has been changed, you need to login to continue',
              'info')
        logout_user()
        return redirect(url_for('authentication_pages.login'))

    # Render the password change form
    return render_template('authentication/change_password.html', form=form)


@authentication_pages.route('/logout', strict_slashes=False)
def logout():
    """ Defines the method for logout operation"""
    logout_user()  # Use the inbuilt logout function to destroy the session

    # Redirect the user to the home page
    return redirect(url_for('common_pages.index'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    """
     Defines a handler for instances where a user accesses a page that requires
     login without being logged in the system
    """
    # Add proper flash message and redirect the user to the login page
    flash('You need to login to view this page', 'warning')
    return redirect(url_for('authentication_pages.login'))
