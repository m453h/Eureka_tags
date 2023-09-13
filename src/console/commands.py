import os
import typer
import pymysql
from flask import Flask
from flask_bcrypt import Bcrypt
from pymysql import IntegrityError

# Initial configuration for the database connection
db_config = {
    'host': 'localhost',
    'user': os.getenv('EUREKA_DB_USER'),
    'password': os.environ.get('EUREKA_DB_PASSWORD'),
    'db': os.environ.get('EUREKA_DB_NAME'),
    'cursorclass': pymysql.cursors.DictCursor
}

# Initialize the database and command line application
db = pymysql.connect(**db_config)
cmd = typer.Typer()


@cmd.command()
def create_admin_account():
    """ Defines the method for creating a new admin account """
    # Fetch admin role id that will be used to create the account
    role_id = fetch_admin_role_id()

    # When admin role Id is none display error message to notify the user
    # to initialize roles first
    if role_id is None:
        print("Error: Please initialize account roles before proceeding")
        return None

    # Prompt user to enter full name, email and password
    full_name = typer.prompt("Full name")
    email = typer.prompt("E-mail")
    password = typer.prompt("Password")

    # Initialize Flask application instance and Bcrypt that will be use to
    # hash the user password
    app = Flask(__name__)
    app.app_context().push()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Record the user account details, we use try and except to check if the
    # email supplied is already used
    try:
        add_admin_account(email, full_name, "A", hashed_password, "2")
        print("Account has been created you may login the e-mail supplied")
    except IntegrityError:
        print("The e-mail you supplied is already registered")


@cmd.command()
def initialize_roles():
    """ Defines the method for initializing user roles """
    # Check if the current state of the database contains any roles
    # if it does then notify the user that the action will not be done
    if fetch_current_roles():
        print("Initializing roles...")
        insert_default_roles("Admin")
        insert_default_roles("User")
        print("All roles are set...")
    else:
        print("Roles already set, no need to re-initialize")


def fetch_current_roles():
    """ Defines the method for fetching current user roles in the database """
    try:
        with db.cursor() as cursor:
            # The SQL query to fetch all the existing roles in the database
            raw_query = "SELECT * FROM role;"

            # Execute the query
            cursor.execute(raw_query)

            # Fetch the results
            result = cursor.fetchall()

            if result == ():
                return True
    finally:
        pass
    return False


def fetch_admin_role_id():
    """ Defines the method for fetching the Admin role Id """
    try:
        with db.cursor() as cursor:
            # The SQL query to fetch the Admin role ID from the database
            raw_query = "SELECT id FROM role WHERE description='Admin';"

            # Execute the query
            cursor.execute(raw_query)

            # Fetch the results
            result = cursor.fetchone()
            if result is None:
                return None
            return result.get('id')
    finally:
        pass


def insert_default_roles(description):
    """
        Defines the method for adding a user role to the database

        Args:
            description (String): The name of the role to add to the database
    """
    try:
        with db.cursor() as cursor:
            # Create an SQL query for inserting a new role
            insert_query = "INSERT INTO role (description, date_created, " \
                           "date_updated) VALUES (%s, NOW(), NOW()) "

            # Execute the query with the data
            cursor.execute(insert_query, (description,))

            # Commit the transaction
            db.commit()
            return True
    finally:
        pass


def add_admin_account(email, full_name, account_status, password, role_id):
    """
        Defines the method for adding an admin account to the database

        Args:
            email (String): The e-mail (username) of the administrator
            full_name (String): The full name of the administrator
            account_status (String): The status of the admin user account
            password (String): The password for the admin user account
            role_id (String): The id of the admin user role
    """
    try:
        with db.cursor() as cursor:
            # Create an SQL query for inserting a new user account
            insert_query = "INSERT INTO user (email, full_name, " \
                           "account_status, password, role_id," \
                           "date_created, has_password_reset_token) " \
                           "VALUES (%s, %s, %s, %s, %s, NOW(), 0) "

            # Execute the query with the data
            cursor.execute(insert_query, (email, full_name, account_status,
                                          password, role_id,))

            # Commit the transaction
            db.commit()
            return True
    finally:
        pass


if __name__ == "__main__":
    cmd()
