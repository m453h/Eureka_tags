#!/usr/bin/python3
""" Starts a Flash Web Application """
import markdown
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import desc, text, or_

from src import db
from src.models.post import Post
from src.models.tag import Tag
from src.web.admin.forms import TagForm
from src.web.user.forms import PostForm

manage_tags_pages = Blueprint('manage_tags_pages', __name__,
                              template_folder='templates',
                              url_prefix='/manage-tags')


@manage_tags_pages.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    tags = Tag.query.paginate(page=page, per_page=10)
    return render_template('manage_tags_pages/index.html', tags=tags)


@manage_tags_pages.route('/add/', strict_slashes=False,
                         methods=['GET', 'POST'])
@login_required
def add():
    form = TagForm()
    if request.method == 'POST' and form.validate():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash('Your tag has been created!', 'success')
        return redirect(url_for('manage_tags_pages.index'))
    return render_template('manage_tags_pages/form.html',
                           form=form, title="Add New Tag")


@manage_tags_pages.route('/edit/<int:tag_id>', strict_slashes=False,
                         methods=['GET', 'POST'])
@login_required
def edit(tag_id):
    q = db.session.query(Tag).filter(Tag.id == tag_id)
    tag = q.first()

    if tag:
        form = TagForm(formdata=request.form, obj=tag)

        if request.method == 'POST' and form.validate():
            tag.name = form.name.data
            db.session.commit()

            flash('Your tag has been updated!', 'success')
            return redirect(url_for('manage_tags_pages.index'))
        return render_template('manage_tags_pages/form.html',
                               form=form, title="Edit Existing Tag")
    else:
        return 'Error loading #{id}'.format(id=id)


@manage_tags_pages.route('/delete/<int:tag_id>', strict_slashes=False,
                         methods=['GET'])
@login_required
def delete(tag_id):
    q = db.session.query(Tag).filter(Tag.id == tag_id)
    tag = q.first()

    if tag:
        db.session.delete(tag)
        db.session.commit()

        flash('Your tag has been removed!', 'success')
        return redirect(url_for('manage_tags_pages.index'))
    else:
        return 'Error loading #{id}'.format(id=id)


