#!/usr/bin/python3
""" Defines a module for the administration of tags """
from flask import render_template, Blueprint, flash, redirect, url_for, \
    request, abort
from flask_login import login_required
from src import db
from src.models.tag import Tag
from src.web.admin.forms import TagForm

# Create blueprint for managing tags
manage_tags_pages = Blueprint('manage_tags_pages', __name__,
                              template_folder='templates',
                              url_prefix='/manage-tags')


@manage_tags_pages.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
    """ Defines the method that lists all tags """

    # Get the current page from request query parameter
    # set 1 as the default page number
    page = request.args.get('page', 1, type=int)

    # Query for all tags paginated with a maximum of 10 posts per page
    tags = Tag.query.paginate(page=page, per_page=10)

    # Render the HTML to display the results
    return render_template('manage_tags_pages/index.html', tags=tags)


@manage_tags_pages.route('/add/', strict_slashes=False,
                         methods=['GET', 'POST'])
@login_required
def add():
    """ Defines the method that adds tags """
    # Initialize the tag management form
    form = TagForm()

    # If the request method is POST and form is valid then proceed to store
    # the data in the database
    if request.method == 'POST' and form.validate():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()

        # Add a flash message and redirect user to the list of posts
        flash('Your tag has been created!', 'success')
        return redirect(url_for('manage_tags_pages.index'))

    # Render the add new tag form
    return render_template('manage_tags_pages/form.html',
                           form=form, title="Add New Tag")


@manage_tags_pages.route('/edit/<int:tag_id>', strict_slashes=False,
                         methods=['GET', 'POST'])
@login_required
def edit(tag_id):
    """
    Defines the method that edits an existing tag

    Args:
        tag_id (String): The id of the tag to edit
    """

    # Query the selected tag for editing in the database by the given Id
    query = db.session.query(Tag).filter(Tag.id == tag_id)

    # Get the first tag matching the query result
    tag = query.first()

    # If the tag exists then proceed with form operations
    if tag:
        # Initialize the form with fetched data from the database
        form = TagForm(formdata=request.form, obj=tag)

        # If the request method is POST and form is valid then proceed to store
        # the data in the database
        if request.method == 'POST' and form.validate():
            tag.name = form.name.data
            db.session.commit()

            # Add a flash message and redirect user to the list of tags
            flash('Your tag has been updated!', 'success')
            return redirect(url_for('manage_tags_pages.index'))

        # Render the form display
        return render_template('manage_tags_pages/form.html',
                               form=form, title="Edit Existing Tag")
    else:
        abort(404)  # Throw 404 not found when supplied with invalid Id


@manage_tags_pages.route('/delete/<int:tag_id>', strict_slashes=False,
                         methods=['GET'])
@login_required
def delete(tag_id):
    """
    Defines the method that deletes an existing tag

    Args:
        tag_id (String): The id of the tag to delete
    """

    # Query the selected tag for deleting in the database by the given Id
    query = db.session.query(Tag).filter(Tag.id == tag_id)

    # Get the first tag matching the query result
    tag = query.first()

    if tag:
        # Remove the tag and commit changes to the database
        db.session.delete(tag)
        db.session.commit()

        # Add a flash message and redirect user to the list of tags
        flash('Your tag has been removed!', 'success')
        return redirect(url_for('manage_tags_pages.index'))
    else:
        abort(404)  # Throw 404 not found when supplied with invalid Id
