#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for
from web.authentication.forms import RegistrationForm, LoginForm

authentication_pages = Blueprint('authentication_pages', __name__,
                                 template_folder='templates')


@authentication_pages.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'mnkotagu@gmail.com' and form.password.data == '123456':
            flash('You have successfully logged in', 'success')
            return redirect(url_for('dashboard_pages.index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('authentication/login.html', form=form)


@authentication_pages.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('You have successfully created your account', 'success')
        return redirect(url_for('authentication_pages.login'))
    return render_template('authentication/register.html', form=form)


@authentication_pages.route('/reset-password', strict_slashes=False)
def reset():
    return render_template('authentication/password_reset.html')
