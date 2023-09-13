#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from src import db
from src.models.user import User
from src.web.admin.forms import UserForm

manage_users_pages = Blueprint('manage_users_pages', __name__,
                               template_folder='templates',
                               url_prefix='/manage-users')


@manage_users_pages.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10)
    return render_template('manage_users_pages/index.html', users=users)


@manage_users_pages.route('/edit/<int:user_id>', strict_slashes=False,
                          methods=['GET', 'POST'])
@login_required
def edit(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()

    if user:
        form = UserForm(formdata=request.form, obj=user)

        if request.method == 'POST' and form.validate():
            user.full_name = form.full_name.data
            user.email = form.email.data
            try:
                db.session.commit()
                flash('User account has been updated!', 'success')
            except IntegrityError:
                flash('Could not update user account details, please use a '
                      'different e-mail address',
                      'danger')
            return redirect(url_for('manage_users_pages.index'))
        return render_template('manage_users_pages/form.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@manage_users_pages.route('/delete/<int:user_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def delete(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()
    if user.id == current_user.id:
        flash('You can not delete your own account !', 'danger')
        return redirect(url_for('manage_users_pages.index'))

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            flash('The user account has been removed !', 'success')
        except IntegrityError:
            flash('Can not delete an account with active posts !', 'danger')

        return redirect(url_for('manage_users_pages.index'))
    else:
        return 'Error loading #{id}'.format(id=id)


@manage_users_pages.route('/block/<int:user_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def block(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()
    if user.id == current_user.id:
        flash('You can not block your own account !', 'danger')
        return redirect(url_for('manage_users_pages.index'))

    if user:
        user.account_status = "B"
        db.session.commit()
        flash('The user account has been blocked !', 'success')
        return redirect(url_for('manage_users_pages.index'))
    else:
        return 'Error loading #{id}'.format(id=id)


@manage_users_pages.route('/unblock/<int:user_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def unblock(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()
    if user.id == current_user.id:
        flash('You can not block your own account !', 'danger')
        return redirect(url_for('manage_users_pages.index'))

    if user:
        user.account_status = "A"
        db.session.commit()
        flash('The user account has been unblocked !', 'success')
        return redirect(url_for('manage_users_pages.index'))
    else:
        return 'Error loading #{id}'.format(id=id)
