#!/usr/bin/python3
""" Defines a module for displaying the dashboard for logged in users """
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import desc, func
from src import db
from src.models.post import Post
from src.models.tag import Tag
from src.models.user import User
from src.web.user.forms import PostForm

# Create blueprint for the dashboard pages
dashboard_pages = Blueprint('dashboard_pages', __name__,
                            template_folder='templates',
                            url_prefix='/dashboard')


@dashboard_pages.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
    """ Defines the method for handling the user dashboard display """

    # If the current role is "User" then move towards displaying
    # the User dashboard
    if current_user.current_role == "User":
        # Render the form for creating a new post
        form = PostForm()

        # Attempt to get selected tags from URL parameter, this would help
        # modify the query that renders posts on the dashboard
        tag = request.args.to_dict().get('t')

        # If the Create post is submitted and is valid then create a new post
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id,
                        is_public=form.is_public.data)

            # Initialize the tags under a post to an empty list
            post.tags = []
            # Iterate on the tags selected by the user in the create post
            # form and append them to the post model
            for tag in form.tags.data:
                post.tags.append(tag)

            # Add the post to the database and commit the changes
            db.session.add(post)
            db.session.commit()

            # Add a flash message to display the successful completion
            # of creating a new post
            flash('Your post has been created!', 'success')
            return redirect(url_for('dashboard_pages.index'))

        # If form was not submitted then create a new query to
        # retrieve relevant posts
        post_query = Post.query.\
            filter_by(user_id=current_user.id).\
            order_by(desc(Post.date_created))

        # If there was a tag from the url query parameters then modify the
        # query to include them when searching in the database
        if tag is not None:
            post_query = post_query.join(Post.tags) \
                .filter(Tag.name == tag) \

        # Get the current page from request query parameter
        # set 1 as the default page number
        page = request.args.get('page', 1, type=int)

        # Paginate the results with the maximum of 4 posts per page
        my_posts = post_query.paginate(page=page, per_page=4)

        # Render the dashboard
        return render_template('dashboard/index.html', form=form,
                               my_posts=my_posts)
    else:
        # Since the user role is not "User" we assume that they are "Admin
        # thus render the admin dashboard

        # Query for the total number of posts in the database
        post_count = db.session.query(Post).count()

        # Query for the total number of tags in the database
        tags_count = db.session.query(Tag).count()

        # Query for the total number of users with active account status
        active_users_count = db.session.query(User) \
            .filter(User.account_status == "A") \
            .count()

        # Query for the total number of users with inactive account status
        inactive_users_count = db.session.query(User) \
            .filter(User.account_status == "I") \
            .count()

        # Write the SQLAlchemy query for getting a summary of daily posts
        query = db.session.query(
            func.count(Post.id).label('total'),
            func.date(Post.date_created).label('date_created')
        ).group_by(func.date(Post.date_created)).order_by(
            func.date(Post.date_created).desc())

        # Execute the query and fetch the results
        results = query.all()
        date_results = []
        total_results = []

        # Format the query results for rendering in JavaScript e-chart library
        for result in results:
            formatted_date = result.date_created.strftime("%d-%m-%Y")
            date_results.append("'{}'".format(formatted_date))
            total_results.append(str(result.total))

        date_results = ", ".join(date_results)
        total_results = ", ".join(total_results)

        # Include all the data in the total variable which is going to be
        # rendered in the dashboard template
        totals = {
            'posts': post_count,
            'tags': tags_count,
            'active_users': active_users_count,
            'inactive_users': inactive_users_count,
            'post_dates': date_results,
            'post_count':  total_results
        }

        # Render the admin dashboard page
        return render_template('dashboard/admin.html', totals=totals)
