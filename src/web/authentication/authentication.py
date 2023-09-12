#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for

from src.models.user import User
from src import db, bcrypt, login_manager, mail, app
from src.web.authentication.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user
from flask_mail import Message

authentication_pages = Blueprint('authentication_pages', __name__,
                                 template_folder='templates')


@authentication_pages.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard_pages.index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('authentication/login.html', form=form)


@authentication_pages.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,
                    full_name=form.full_name.data,
                    account_status="I",
                    role_id="1",
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_activation_email(user)
        flash('You are account has been created, please check your e-mail for your account activation instructions',
              'success')
        return redirect(url_for('authentication_pages.login'))
    return render_template('authentication/register.html', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    html_body = render_template('authentication/password_reset_email.html',
                                recipient_name=user.full_name,
                                reset_link=url_for('authentication_pages.reset_token', token=token, _external=True)
                                )
    msg.html = html_body
    mail.send(msg)


def send_activation_email(user):
    token = user.get_reset_token()
    msg = Message('Account Activation', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    html_body = render_template('authentication/activation_email.html',
                                recipient_name=user.full_name,
                                activation_link=url_for('authentication_pages.activation_token', token=token,
                                                        _external=True))
    msg.html = html_body
    mail.send(msg)


@authentication_pages.route('/reset-password', strict_slashes=False, methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user.has_password_reset_token = True
        db.session.commit()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('authentication_pages.login'))

    return render_template('authentication/password_reset_request.html', form=form)


@authentication_pages.route('/reset-password/<token>', strict_slashes=False, methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    user = User.verify_reset_token(token)
    if user is None or not user.has_password_reset_token:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('authentication_pages.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        user.has_password_reset_token = False
        db.session.commit()
        flash('Your password has been updated, You are now able to log in!', 'success')
        return redirect(url_for('authentication_pages.login'))
    return render_template('authentication/password_reset_token.html', form=form)


@authentication_pages.route('/activate/<token>', strict_slashes=False, methods=['GET', 'POST'])
def activation_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    user = User.verify_reset_token(token)
    print(user)
    if user is None or not user.account_status == "I":
        flash('That is an invalid or expired token, please reset your password', 'warning')
        return redirect(url_for('authentication_pages.reset_request'))

    user.account_status = 'A'
    db.session.commit()
    flash('Your account has been successfully activated, You are now able to log in!', 'success')
    return redirect(url_for('authentication_pages.login'))


@authentication_pages.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('common_pages.index'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You need to login to view this page', 'warning')
    return redirect(url_for('authentication_pages.login'))
