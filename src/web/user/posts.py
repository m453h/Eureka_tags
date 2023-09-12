#!/usr/bin/python3
""" Starts a Flash Web Application """
import markdown
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import desc, text, or_

from src import db
from src.models.post import Post
from src.web.user.forms import PostForm

posts_pages = Blueprint('posts_pages', __name__,
                        template_folder='templates', url_prefix='/post')


@posts_pages.route('/edit/<int:post_id>', strict_slashes=False, methods=['GET', 'POST'])
@login_required
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
@login_required
def view(post_id):
    q = db.session.query(Post).filter(Post.id == post_id)
    post = q.first()

    if post:
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
    page = request.args.get('page', 1, type=int)
    my_posts = posts_query.paginate(page=page, per_page=4)

    return render_template('posts_pages/search_results.html', my_posts=my_posts)
