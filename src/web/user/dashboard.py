#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint

from src.web.user.forms import PostForm

dashboard_pages = Blueprint('dashboard_pages', __name__,
                            template_folder='templates', url_prefix='/dashboard')


@dashboard_pages.route('/', strict_slashes=False, )
def index():
    form = PostForm()
    return render_template('dashboard/index.html', form=form)
