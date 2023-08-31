#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint

common_pages = Blueprint('common_pages', __name__,
                         template_folder='templates')


@common_pages.route('/', strict_slashes=False)
def index():
    return render_template('common_pages/index.html')
