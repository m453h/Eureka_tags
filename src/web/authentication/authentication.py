#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for

from src.models.user import User
from src import db, bcrypt
from src.web.authentication.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user

authentication_pages = Blueprint('authentication_pages', __name__,
                                 template_folder='templates')


@authentication_pages.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
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
                    account_status="A",
                    role_id="1",
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You are account has been created, you are now able to login', 'success')
        return redirect(url_for('authentication_pages.login'))
    return render_template('authentication/register.html', form=form)


@authentication_pages.route('/reset-password', strict_slashes=False)
def reset():
    return render_template('authentication/password_reset.html')


@authentication_pages.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('common_pages.index'))
