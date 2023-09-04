#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user

from src import db
from src.models.post import Post
from src.models.tag import Tag
from src.web.user.forms import PostForm
from keybert import KeyBERT

posts_pages = Blueprint('posts_pages', __name__,
                        template_folder='templates', url_prefix='/post')


@posts_pages.route('/new', strict_slashes=False, methods=['GET', 'POST'])
def create():
    form = PostForm()
    if form.validate_on_submit():
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(form.title.data, top_n=5)
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        tag = Tag(name=keywords[0][0])
        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created!', 'success')
        # return redirect(url_for('dashboard_pages.index'))

    return render_template('posts_pages/create.html', form=form)
