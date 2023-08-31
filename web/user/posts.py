#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint

posts_pages = Blueprint('posts_pages', __name__,
                        template_folder='templates', url_prefix='/')


@posts_pages.route('create-post', strict_slashes=False)
def index():
    return render_template('posts_pages/create.html')
