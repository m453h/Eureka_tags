<p align="center">
  <a href="https://gofiber.io">
    <picture>
      <source height="125" media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/m453h/Eureka_tags/master/src/static/images/app_logo_alt.png">
      <img height="125" alt="Eureka Tags" src="https://raw.githubusercontent.com/m453h/Eureka_tags/master/src/static/images/app_logo_alt.png">
    </picture>
  </a>
  <br>
</p>

## Eureka Tags
Eureka Tags is a web-based application that aims to help individuals in various tech-related domains document and organize solutions to various problems they’ve encountered.

## Installation
### Downloading and installing steps:
1. Make sure you have Python 3.8 or above and pip (version 23.2.1 or above) and MySQL (version 8.0.34 or above) installed and clone the project repository
   <pre>
   git@github.com:m453h/Eureka_tags.git
   </pre>
2. Change into the clone project directory and run the following command to install the project dependencies
    <pre>
    pip install -r requirements.txt
   </pre>
3. Create the following environment variables:
     - EUREKA_DB_NAME: The name of the database used by the application
     - EUREKA_DB_USER: The username of the database used by the application;
     - EUREKA_DB_PASSWORD: The password of the database used by the application
     - MAIL_SERVER: The server used to send e-mail notifications
     - MAIL_PORT: The port of the mail server used to sent notifications
     - EMAIL_USER: The user account of the email used by the application to send notifications 
     - EMAIL_PASSWORD: The password of the email used by the application to send notifications
     - SECRET_KEY: This is a key that is used for securely signing the session cookie and other security related needs of the application
4. Make sure your database is set up correctly, change to the project sources directory (src) and run the ```flask db upgrade``` command to create the tables used by the application
    <pre>
    cd [PROJECT_DIRECTORY>]/src
    flask db upgrade
   </pre>
5. Change to the project console directory inside the project sources directory (src) and run the ```initialize-roles``` and ``` create-admin-account ``` commands to set up the initial data needed to run the application.
    <pre>
     cd [PROJECT_DIRECTORY>]/src/console
     python commands.py initialize-roles
     python commands.py create-admin-account 
   </pre>
6. Change to the project sources directory (src) and run the application 
    <pre>
   flask --app app run
   </pre>
    You may also run the application using any application server of your choice e.g. for gunicorn use
    <pre>
    gunicorn --bind 0.0.0.0:5000 src.app:app
   </pre>
## Usage
## Contributing
## Related projects
## Licensing