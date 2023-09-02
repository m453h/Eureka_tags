#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user


common_pages = Blueprint('common_pages', __name__,
                         template_folder='templates')


@common_pages.route('/', strict_slashes=False)
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    return render_template('common_pages/index.html')
