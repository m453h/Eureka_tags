#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import current_user
import markdown
from sqlalchemy import desc, text, or_

from src import db
from src.models.post import Post
from src.models.tag import Tag
from src.web.user.forms import PostForm

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
        flash('Your are editing an existing post!', 'info')
        return render_template('posts_pages/edit.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@posts_pages.route('/view/<int:post_id>', strict_slashes=False, methods=['GET'])
def view(post_id):
    q = db.session.query(Post).filter(Post.id == post_id)
    post = q.first()

    if post:
        content = markdown.markdown(post.content)
        post.content = content
        return render_template('posts_pages/view.html', post=post)
    else:
        return 'Error loading #{id}'.format(id=id)


@posts_pages.route('/delete/<int:post_id>', strict_slashes=False, methods=['GET'])
def delete(post_id):
    q = db.session.query(Post).filter(Post.id == post_id)
    post = q.first()

    if post:
        post.tags.clear()
        db.session.delete(post)
        db.session.commit()

        flash('Your post has been removed!', 'success')
        return redirect(url_for('dashboard_pages.index'))
    else:
        return 'Error loading #{id}'.format(id=id)


@posts_pages.route('/search', strict_slashes=False, methods=['GET'])
def search():
    search_content = request.args.get('q')
    my_posts = Post.query. \
        filter_by(user_id=current_user.id) \
        .filter(
                or_(
                    text("title LIKE :content"),
                    text("content LIKE :content")
                )
            ) \
        .params(content=f"%{search_content}%") \
        .order_by(desc(Post.date_created)) \
        .all()

    return render_template('posts_pages/search_results.html', my_posts=my_posts)
