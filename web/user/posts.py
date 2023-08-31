#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint

dashboard_pages = Blueprint('dashboard_pages', __name__,
                            template_folder='templates', url_prefix='/dashboard')


@dashboard_pages.route('/', strict_slashes=False)
def index():
    return render_template('dashboard/index.html')
