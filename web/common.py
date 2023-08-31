#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint

authentication_pages = Blueprint('authentication_pages', __name__,
                                 template_folder='templates')


@authentication_pages.route('/', strict_slashes=False)
def index():
    return render_template('index.html')


@authentication_pages.route('/login', strict_slashes=False)
def login():
    return render_template('login.html')


@authentication_pages.route('/register', strict_slashes=False)
def register():
    return render_template('register.html')


@authentication_pages.route('/reset-password', strict_slashes=False)
def reset():
    return render_template('password_reset.html')


