#!/usr/bin/python3
""" Defines a module for the administration of user accounts """
from flask import render_template, Blueprint, flash, redirect, url_for, \
    request, abort
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
    # Get the current page from request query parameter
    # set 1 as the default page number
    page = request.args.get('page', 1, type=int)

    # Query for all users paginated with a maximum of 10 posts per page
    users = User.query.paginate(page=page, per_page=10)

    # Render the HTML to display the results
    return render_template('manage_users_pages/index.html', users=users)


@manage_users_pages.route('/edit/<int:user_id>', strict_slashes=False,
                          methods=['GET', 'POST'])
@login_required
def edit(user_id):
    # Query the selected user for editing in the database by the given Id
    query = db.session.query(User).filter(User.id == user_id)

    # Get the first tag matching the query result
    user = query.first()

    # If the user exists then proceed with form operations
    if user:
        # Initialize the form with fetched data from the database
        form = UserForm(formdata=request.form, obj=user)

        # If the request method is POST and form is valid then proceed to store
        # the data in the database
        if request.method == 'POST' and form.validate():
            user.full_name = form.full_name.data
            user.email = form.email.data
            # Try to commit changes to the database, the exception that we
            # might encounter is an IntegrityError exception
            try:
                db.session.commit()
                flash('User account has been updated!', 'success')
            except IntegrityError:
                flash('Could not update user account details, please use a '
                      'different e-mail address',
                      'danger')
            # Redirect user to the list of users
            return redirect(url_for('manage_users_pages.index'))
        # Render form for editing user account details
        return render_template('manage_users_pages/form.html', form=form)
    else:
        abort(404)  # Throw 404 not found when supplied with invalid Id


@manage_users_pages.route('/delete/<int:user_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def delete(user_id):
    query = db.session.query(User).filter(User.id == user_id)
    user = query.first()

    # If the account selected for deletion is the current logged in user
    # then deny this action as it may cause the admin to be locked out
    if user.id == current_user.id:
        flash('You can not delete your own account !', 'danger')

        # Redirect user to list of users page
        return redirect(url_for('manage_users_pages.index'))

    # Try to delete the user account the exception we might encounter here is
    # the IntegrityError in which we would be trying to delete a user account
    # that has posts associated with it.
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            flash('The user account has been removed !', 'success')
        except IntegrityError:
            flash('Can not delete an account with active posts !', 'danger')

        # Redirect user to list of users page
        return redirect(url_for('manage_users_pages.index'))
    else:
        abort(404)  # Throw 404 not found when supplied with invalid Id


@manage_users_pages.route('/block/<int:user_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def block(user_id):
    query = db.session.query(User).filter(User.id == user_id)
    user = query.first()

    # If the account selected for status modification is the current
    # logged in user then deny this action
    if user.id == current_user.id:
        flash('You can not block your own account !', 'danger')

        # Redirect user to list of users page
        return redirect(url_for('manage_users_pages.index'))

    # If the User exists then update the account status
    if user:
        user.account_status = "B"
        db.session.commit()  # Save changes to the database
        # Add proper flash message after committing changes to the database
        flash('The user account has been blocked !', 'success')

        # Redirect user to list of users page
        return redirect(url_for('manage_users_pages.index'))
    else:
        abort(404)  # Throw 404 not found when supplied with invalid Id


@manage_users_pages.route('/unblock/<int:user_id>', strict_slashes=False,
                          methods=['GET'])
@login_required
def unblock(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()

    # If the account selected for status modification is the current
    # logged in user then deny this action
    if user.id == current_user.id:
        flash('You can not block your own account !', 'danger')

        # Redirect user to list of users page
        return redirect(url_for('manage_users_pages.index'))

    # If the User exists then update the account status
    if user:
        user.account_status = "A"
        db.session.commit()  # Save changes to the database

        # Add proper flash message after committing change to the database
        flash('The user account has been unblocked !', 'success')

        # Redirect user to list of users page
        return redirect(url_for('manage_users_pages.index'))
    else:
        abort(404)  # Throw 404 not found when supplied with invalid Id
