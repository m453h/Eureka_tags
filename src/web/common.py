#!/usr/bin/python3
""" Starts a Flash Web Application """
from datetime import datetime

import bleach
from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user

from src import app, db
from src.models.post import Post

common_pages = Blueprint('common_pages', __name__,
                         template_folder='templates')


@common_pages.route('/', strict_slashes=False)
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    return render_template('common_pages/index.html')


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


def sanitize_html(value):
    allowed_tags = {'pre', 'code'}
    allowed_attributes = {}
    return bleach.clean(value, tags=allowed_tags, attributes=allowed_attributes)


app.jinja_env.filters['sanitize'] = sanitize_html
