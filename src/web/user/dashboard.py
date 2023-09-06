#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user

from src import db
from src.models.post import Post
from src.web.user.forms import PostForm

dashboard_pages = Blueprint('dashboard_pages', __name__,
                            template_folder='templates', url_prefix='/dashboard')


@dashboard_pages.route('/', strict_slashes=False, methods=['GET','POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        print(form.tags.data)
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, is_public=form.is_public.data)
        for tag in form.tags.data:
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('dashboard_pages.index'))
    return render_template('dashboard/index.html', form=form)
