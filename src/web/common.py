#!/usr/bin/python3
""" Defines the module for the application landing page """
from datetime import datetime

import bleach
import markdown
from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user

from src import app

# Create blueprint for the common pages
common_pages = Blueprint('common_pages', __name__,
                         template_folder='templates')


@common_pages.route('/', strict_slashes=False)
def index():
    """
    Defines the method that renders the application landing page
    """
    # If the current user is logged in then redirect them
    # to the application dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_pages.index'))

    # Render the application landing page
    return render_template('common_pages/index.html')


@app.context_processor
def inject_now():
    """
        Defines the method that injects various objects to the jinja
        templating engine
    """
    return {'now': datetime.utcnow()}


def sanitize_html(value):
    """
    Defines the method that Sanitizes and filters HTML content to remove
    potentially unsafe elements and attributes while allowing specific safe
    elements and attributes.

    This function uses the 'bleach' library to clean and filter HTML content,
    removing any potentially harmful elements and attributes. It allows only
    specific safe elements and attributes to be included in the
    sanitized output.

    Args:
        value (str): The HTML content to be sanitized.

    Returns:
        str: The sanitized HTML content.

    """
    allowed_tags = {'pre', 'code', 'p', 'strong', 'em', 'h1', 'a',
                    'abbr', 'acronym', 'b', 'blockquote', 'li', 'strong',
                    'ul', 'br', 'hr'}
    allowed_attributes = {
        '*': ['class'],
        'a': ['href', 'rel', 'title'],
    }
    return bleach.clean(value, tags=allowed_tags,
                        attributes=allowed_attributes)


def markdown_to_html(value):
    """
       Converts Markdown-formatted text to HTML.

       This function takes Markdown-formatted text as input and converts it to
       HTML format using the 'markdown' library. Markdown is a lightweight
       markup language that allows you to write plain text that is easily
       transformed into HTML.

       Args:
           value (str): The Markdown-formatted text to be converted to HTML.

       Returns:
           str: The HTML representation of the input Markdown text.
    """
    return markdown.markdown(value)


# Add the functions to sanitize and render markdown to
# HTML in the Jinja Templating engine
app.jinja_env.filters['sanitize'] = sanitize_html
app.jinja_env.filters['markdown_to_html'] = markdown_to_html
