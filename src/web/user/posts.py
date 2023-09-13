#!/usr/bin/python3
""" Defines a module for the user posts """
from flask import render_template, Blueprint, flash, redirect, url_for, \
    request, abort
from flask_login import current_user, login_required
from sqlalchemy import desc, text, or_
from src import db
from src.models.post import Post
from src.web.user.forms import PostForm

# Create blueprint for the user posts pages
posts_pages = Blueprint('posts_pages', __name__,
                        template_folder='templates', url_prefix='/post')


@posts_pages.route('/edit/<int:post_id>', strict_slashes=False,
                   methods=['GET', 'POST'])
@login_required
def edit(post_id):
    """
    Defines the method for editing a user post

    Args:
        post_id (int): The id of the post to edit
    """
    # Query the selected post for editing in the database by the given Id
    query = db.session.query(Post).filter(Post.id == post_id)

    # Get the first post matching the query result
    post = query.first()

    # If the post exists then proceed with form operations
    if post:
        # Initialize the form with fetched data from the database
        form = PostForm(formdata=request.form, obj=post)

        # If the request method is POST and form is valid then proceed to store
        # the data in the database
        if request.method == 'POST' and form.validate():
            post.title = form.title.data
            post.content = form.content.data
            post.is_public = form.is_public.data
            post.tags.clear()
            db.session.commit()

            # Add new tags selected by user to the database
            for tag in form.tags.data:
                post.tags.append(tag)
                print("Adding: " + tag.name)
            db.session.commit()

            # Add a flash message and redirect user to the list of posts
            flash('Your post has been updated!', 'success')
            return redirect(url_for('dashboard_pages.index'))

        form.tags.process_data(post.tags)  # Process the tags to be displayed

        # Always display a flash message when editing a post
        flash('Your are editing an existing post!', 'info')

        # Render the form display
        return render_template('posts_pages/edit.html', form=form)
    else:
        abort(404)  # Throw 404 Not Found


@posts_pages.route('/view/<int:post_id>', strict_slashes=False,
                   methods=['GET'])
@login_required
def view(post_id):
    """
    Defines the method for viewing a user post

    Args:
        post_id (int): The id of the post to edit
    """
    # Query the selected post for editing in the database by the given Id
    query = db.session.query(Post).filter(Post.id == post_id)

    # Get the first post matching the query result
    post = query.first()

    # If the post exists then proceed with form operations
    if post:
        # Render the page to view the post
        return render_template('posts_pages/view.html', post=post)
    else:
        abort(404)  # Throw 404 Not Found


@posts_pages.route('/delete/<int:post_id>', strict_slashes=False,
                   methods=['GET'])
def delete(post_id):
    """
    Defines the method for deleting a user post

    Args:
        post_id (int): The id of the post to edit
    """
    # Query the selected post for deleting in the database by the given Id
    query = db.session.query(Post).filter(Post.id == post_id)

    # Get the first post matching the query result
    post = query.first()

    # If the post exists then proceed with delete operation
    if post:
        post.tags.clear()  # Remove all tags related with the post
        db.session.delete(post)  # Remove the post
        db.session.commit()  # Commit changes to the database

        # Add a flash message and redirect user to the list of posts
        flash('Your post has been removed!', 'success')
        return redirect(url_for('dashboard_pages.index'))
    else:
        abort(404)  # Throw 404 Not Found


@posts_pages.route('/search', strict_slashes=False, methods=['GET'])
def search():
    """ Defines the method for searching for a user post"""

    # Get the URL parameter sent when the user submits a valid search form
    search_content = request.args.get('q')

    # Define the query to that searches for a post
    posts_query = Post.query. \
        filter_by(user_id=current_user.id) \
        .filter(
          or_(
            text("title LIKE :content"),
            text("content LIKE :content")
          )
        ) \
        .params(content=f"%{search_content}%") \
        .order_by(desc(Post.date_created))

    # Get the current page from request query parameter
    # set 1 as the default page number
    page = request.args.get('page', 1, type=int)

    # Query for all posts paginated with a maximum of 4 posts per page
    my_posts = posts_query.paginate(page=page, per_page=4)

    # Render the HTML to display the results
    return render_template('posts_pages/search_results.html',
                           my_posts=my_posts)
