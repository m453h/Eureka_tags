#!/usr/bin/python3
""" Starts a Flash Web Application """
import requests
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import desc, func

from src import db
from src.models.post import Post
from src.models.tag import Tag
from src.models.user import User
from src.web.user.forms import PostForm

dashboard_pages = Blueprint('dashboard_pages', __name__,
                            template_folder='templates',
                            url_prefix='/dashboard')


@dashboard_pages.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
    if current_user.current_role == "User":
        form = PostForm()
        tag = request.args.to_dict().get('t')
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id,
                        is_public=form.is_public.data)
            post.tags = []
            for tag in form.tags.data:
                post.tags.append(tag)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('dashboard_pages.index'))

        post_query = Post.query.\
            filter_by(user_id=current_user.id).\
            order_by(desc(Post.date_created))

        if tag is not None:
            post_query = post_query.join(Post.tags) \
                .filter(Tag.name == tag) \

        page = request.args.get('page', 1, type=int)
        my_posts = post_query.paginate(page=page, per_page=4)
        return render_template('dashboard/index.html', form=form,
                               my_posts=my_posts)
    else:
        post_count = db.session.query(Post).count()
        tags_count = db.session.query(Tag).count()
        active_users_count = db.session.query(User) \
            .filter(User.account_status == "A") \
            .count()
        inactive_users_count = db.session.query(User) \
            .filter(User.account_status == "I") \
            .count()

        # Write the SQLAlchemy query
        query = db.session.query(
            func.count(Post.id).label('total'),
            func.date(Post.date_created).label('date_created')
        ).group_by(func.date(Post.date_created)).order_by(
            func.date(Post.date_created).desc())

        # Execute the query and fetch the results
        results = query.all()
        date_results = []
        total_results = []
        for result in results:
            formatted_date = result.date_created.strftime("%d-%m-%Y")
            date_results.append("'{}'".format(formatted_date))
            total_results.append(str(result.total))

        date_results = ", ".join(date_results)
        total_results = ", ".join(total_results)

        totals = {
            'posts': post_count,
            'tags': tags_count,
            'active_users': active_users_count,
            'inactive_users': inactive_users_count,
            'post_dates': date_results,
            'post_count':  total_results
        }

        return render_template('dashboard/admin.html', totals=totals)
