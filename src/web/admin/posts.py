#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for, request
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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=10)
    return render_template('manage_posts_pages/index.html', posts=posts)


@manage_posts_pages.route('/edit/<int:post_id>', strict_slashes=False,
                          methods=['GET', 'POST'])
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
            return redirect(url_for('manage_posts_pages.index'))
        form.tags.process_data(post.tags)
        return render_template('manage_posts_pages/form.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@manage_posts_pages.route('/delete/<int:post_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def delete(post_id):
    q = db.session.query(Post).filter(Post.id == post_id)
    post = q.first()

    if post:
        post.tags.clear()
        db.session.delete(post)
        db.session.commit()

        flash('The post has been removed !', 'success')
        return redirect(url_for('manage_posts_pages.index'))
    else:
        return 'Error loading #{id}'.format(id=id)