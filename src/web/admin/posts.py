#!/usr/bin/python3
""" Defines a module for the administration of user posts """
from flask import render_template, Blueprint, flash, redirect, url_for, \
    request, abort
from flask_login import login_required
from src import db
from src.models.post import Post
from src.web.user.forms import PostForm

manage_posts_pages = Blueprint('manage_posts_pages', __name__,
                               template_folder='templates',
                               url_prefix='/manage-posts')


@manage_posts_pages.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
    # Get the current page from request query parameter
    # set 1 as the default page number
    page = request.args.get('page', 1, type=int)

    # Query for all posts paginated with a maximum of 10 posts per page
    posts = Post.query.paginate(page=page, per_page=10)

    # Render the HTML to display the results
    return render_template('manage_posts_pages/index.html', posts=posts)


@manage_posts_pages.route('/edit/<int:post_id>', strict_slashes=False,
                          methods=['GET', 'POST'])
@login_required
def edit(post_id):
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
            post.tags.clear()  # Remove all tags relating to this post
            db.session.commit()

            # Add new tags selected by user to the database
            for tag in form.tags.data:
                post.tags.append(tag)
                print("Adding: " + tag.name)
            db.session.commit()

            # Add a flash message and redirect user to the list of posts
            flash('Your post has been updated!', 'success')
            return redirect(url_for('manage_posts_pages.index'))
        form.tags.process_data(post.tags)  # Process the tags to be displayed
        # Render the form display
        return render_template('manage_posts_pages/form.html', form=form)
    else:
        abort(404)  # Throw 404 Not Found


@manage_posts_pages.route('/delete/<int:post_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def delete(post_id):
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
        flash('The post has been removed !', 'success')
        return redirect(url_for('manage_posts_pages.index'))
    else:
        abort(404)  # Throw 404 Not Found
