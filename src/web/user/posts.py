#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for, request
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


@posts_pages.route('/edit/<int:post_id>', strict_slashes=False, methods=['GET', 'POST'])
def edit(post_id):
    q = db.session.query(Post).filter(Post.id == post_id)
    post = q.first()

    if post:
        form = PostForm(formdata=request.form, obj=post)

        if request.method == 'POST' and form.validate():
            post.title = form.title.data
            post.content = form.content.data
            post.is_public = form.is_public.data
            post.tags.clear()
            db.session.commit()

            for tag in form.tags.data:
                post.tags.append(tag)
                print("Adding: " + tag.name)
            db.session.commit()

            flash('Your post has been updated!', 'success')
            return redirect(url_for('dashboard_pages.index'))
        form.tags.process_data(post.tags)
        return render_template('posts_pages/edit.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
