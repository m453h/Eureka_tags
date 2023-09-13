<p align="center">
  <a href="https://m453h.tech">
    <picture>
      <source  media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/app_logo.png">
      <img alt="Eureka Tags" src="https://raw.githubusercontent.com/m453h/Eureka_tags/master/media/app_logo.png">
    </picture>
  </a>
  <br>
</p>
![Static Badge](https://img.shields.io/badge/Tested%20with-Python%203.8-yellow)
![Static Badge](https://img.shields.io/badge/Tested%20with-MySQL%208.0.34-blue)
![Static Badge](https://img.shields.io/badge/Tested%20with-Ubuntu%2020.04-orange)


## Table of Contents
- [Introduction](#-introduction)
   * [Demo](#-demo)
   * [Project Team](#-project-team)
   * [Motivation](#-motivation)
   * [Blog Post](#-blog-post)
- [Installation](#-installation)
    * [Downloading and installing steps](#-downloading-and-installing-steps)
- [Usage](#-usage)
- [Contributing](#-contributing)
   * [How to contribute](#-how-to-contribute)
   * [Code Style](#-code-style)
- [Related Projects](#-related-projects)
- [Built with](#-built-with)
- [Licensing](#-licensing)

##  🏁 Introduction
Eureka Tags is a web-based application that enables students and professionals in various tech-related fields such as software developers, DevOps engineers, system administrators, and data scientists,  to document and organize solutions to technical problems they’ve encountered. The application provides a concise way to document and organize solutions to these problems so that whenever such a problem is encountered again there would be a central knowledge repository that can be used to retrieve the correct solution, thus saving precious time and increasing productivity.  This application was developed as part of the portfolio project for the Foundations ALX Software Engineering program

### 🚀 Demo
To see Eureka Tags in action click the following [link](http://m453h.tech) and create your account.
### 🤝 Project Team
This project has been developed by Michael Hudson Nkotagu, Connect with the developer via [Github](https://github.com/m453h), [Linked](ww.linkedin.com/in/michael-hudson-nkotagu).

### 💪 Motivation
The motivation for this project stems from the hard lessons I’ve learned through using computers for more than half of my life. Over the course of time, I have come to accept the fact that with computers things can go wrong and they usually go wrong very fast. I remember when I was a kid, my brother and I would spend countless hours trying to install our favourite PC games. We were always learning new things, but we also made some mistakes that resulted in infecting our home computer with viruses or corrupting our files. Having little knowledge about computers and limited internet access we’d often write down in our exercise books the steps we used to solve the numerous problems we encountered and the mistakes that we made so that we’d avoid repeating them the next time.   Similarly, as I started to learn and work with different programming languages I’ve often found myself writing down different solutions to my problems in different places such as notes application, sending myself an e-mail with a description of a solution, and bookmarking pages with different solutions.  The fundamental with this approach in which information is scattered across multiple applications and devices is the fact I’ve often found it difficult to search for the solution I need when I face a problem I suspect I’ve already solved. This problem became more evident as I was learning a lot of new concepts within a short span of time in the ALX Software Engineering programme. Therefore I concluded that things should be better, I should not only find a way to store the solutions to various technical problems I’ve encountered but also easily retrieve them whenever needed. Thus, when it was time to work on my portfolio project it was a foregone conclusion that I would develop Eureka Tags, I believe that this project will help many people working or learning about different tech stacks document numerous solutions to different problems they'll encounter in the exciting journey and consequently boost their productivity by making their documented solutions easy to retrieve whenever they need to refer back to them.

### 📘 Blog Post
To read more about this project click the following [link](https://medium.com/@m453h/difficult-takes-a-day-impossible-takes-a-week-or-two-how-i-developed-eureka-tags-in-two-weeks-8d1be07fc8d4).

## 🔧 Installation
### ⬇️ Downloading and installing steps:
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
## 🤔 Usage
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

## ✅ Contributing
We welcome contributions to improve Eureka Tags! Whether you want to report a bug, request a feature, or submit a pull request with code changes, 
please follow the guidelines outlined below.

### 🔄 How to contribute
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

### 🕺 Code Style
1. This project uses the pycodestyle (version 2.8.*) coding convention
2. Write clear, concise, and well-documented code. Include comments and docstrings to explain your code's functionality.


## 🥂 Related Projects
The following project relate to Eureka Tags: [Larder](https://larder.io/), [Codever](https://www.codever.dev/), and [CarryLinks](https://carrylinks.com/).

## 🛠️ Built With
Technologies used in this project include:
   * Flask
   * Bootstrap 5
   * Markdown
   * MySQL
   * JavaScript
   * jQuery
   * HTML5
   * CSS3
   * Font Awesome
   * eCharts
   * SimpleMDE
   * Select2

For the list of Python dependencies see the [requirements.txt](https://github.com/m453h/Eureka_tags/blob/master/requirements.txt) file.
## ⚖️ Licensing
This project is under the MIT License. See the [LICENSE](https://raw.githubusercontent.com/m453h/Eureka_tags/master/LICENSE.txt) file for the full license text.