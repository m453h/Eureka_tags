<p align="center">
  <a href="https://m453h.tech">
    <picture>
      <source  media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/app_logo.png">
      <img alt="Eureka Tags" src="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/app_logo.png">
    </picture>
  </a>
  <br>
</p>

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
    * [Downloading and installing steps](#downloading-and-installing-steps:)
- [Usage](#usage)
- [Contributing](#contributing)
   * [How to contribute](#how-to-contribute)
   * [Code Style](#code-style)
- [Related Projects](#related-projects)
- [Licensing](#licensing)

## Introduction
Eureka Tags is a web-based application that aims to help individuals in various tech-related domains document and organize solutions to various problems they’ve encountered.

## Installation
### Downloading and installing steps:
1. Make sure you have Python 3.8 or above and pip (version 23.2.1 or above) and MySQL (version 8.0.34 or above) installed and clone the project repository
   <pre>
   git clone git@github.com:m453h/Eureka_tags.git
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
You can run Eureka Tags in your local machine or through your preferred host.
After the initial setup, you can access the application via your preferred
browser. Given that everything is set up correctly, you should see the following page:
<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/application_home_page.png">
      <img alt="Eureka Tags" src="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/application_home_page.png">
    </picture>
  <br>
</p>

Here are a few things that you can do with Eureka Tags:

**1. Create a Post about a solution you've discovered:**
Eureka tags allows you to write down the solution to your problem by using Markdown, it features an easy to you WYSIWYG markdown editor (SimpleMDE). Learn more about the SimpleMDE [here](https://simplemde.com/).
When creating a post about a solution you can choose whether it should be visible to only you or to other users of the application. Eureka tags also allows you to categorize your solutions under a specific tag which could be a programming language, tool or topic.
<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/application_create_post.png">
      <img alt="Eureka Tags" src="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/application_create_post.png">
    </picture>
  <br>
</p>

**2. Search for a solution you previously documented:**
Eureka tags features an easy-to-use search bar that is always visible when you are logged in the application. You can use this search bar to quickly search for a solution to problem you documented to relive that Eureka moment !
You can also browse for all solutions categorized under a certain tag by simply clicking a tag.
<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/application_dashboard.png">
      <img alt="Eureka Tags" src="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/application_dashboard.png">
    </picture>
  <br>
</p>

**3. Edit or delete a post about a solution:** Eureka tags allows you to edit or delete a post you've made documenting a solution to a problem. If you've made a mistake, you don't have to worry you can quickly rectify it.

## Contributing
We welcome contributions to improve Eureka Tags! Whether you want to report a bug, request a feature, or submit a pull request with code changes, 
please follow the guidelines outlined below.

### How to contribute
1. Fork the Repository: Click on the "Fork" button at the top-right corner of the repository's page. This will create a copy of the repository in your GitHub account.

2. Clone the Repository: Clone the forked repository to your local machine using git clone. 
   <pre>
   git clone git@github.com:m453h/Eureka_tags.git
   </pre>

3. Create a Branch: Create a new branch for your contribution. Choose a descriptive name that reflects the purpose of your changes.
4. Make Changes: Make your desired changes to the codebase. Ensure that your changes adhere to the project's coding standards.
5. Commit Changes: Commit your changes with a clear and concise commit message. Use the present tense and a brief description of what your commit does.
6. Push Changes: Push your changes to your forked repository on GitHub.
7. Submit a Pull Request: Go to the Eureka Tag's main repository's page on GitHub and click on the "New Pull Request" button. Provide a clear title and description for your pull request, explaining the purpose and changes made.

### Code Style
1. This project uses the pycodestyle (version 2.8.*) coding convention
2. Write clear, concise, and well-documented code. Include comments and docstrings to explain your code's functionality.


## Related projects
The following project relate to Eureka Tags: [Larder](https://larder.io/), [Codever](https://www.codever.dev/), and [CarryLinks](https://carrylinks.com/).
## Licensing
This project is under the MIT License. See the [LICENSE](https://raw.githubusercontent.com/m453h/Eureka_tags/master/LICENSE.txt) file for the full license text.
