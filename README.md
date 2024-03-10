# Overview

{Important! Do not say in this section that this is college assignment. Talk about what you are trying to accomplish as a software engineer to further your learning.}

I have developed an Exercise and Health Tracking application that uses a SQL Relational Database. It is designed to help users monitor their exercise routines and associated health metrics. It uses user authentication to ensure secure access to individual profiles, data organization using the relational database, and also filtering using date/time. The user can also view a summary and the analytical data if desired.
The user starts by creating an account with a unique username, allowing them to access their data each time they use it. They then log each workout they complete, alongside health measurements such as BMI, weight, and muscle measurements. They can then view this data anytime by going to the dashboard, and can view a summary of their data to see improvements/changes over time.

In part, I created this software because I believed it would showcase the necessary things for the course. However, it is also a program that I personally would, and likely will use. I have used various exercise tracking apps over the years, and have not really liked any of them. I hoped that this program would be more user friendly, at least for myself, and therefore extremey useful.

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](http://youtube.link.goes.here)

# Relational Database

{Describe the relational database you are using.}

{Describe the structure (tables) of the relational database that you created.}

# Development Environment

I used Python as the core programming language for the application, as it is simple but also efficient when creating things such as this.
I used Flask as the web framework, which not only helped me to develop and perfect the application sooner, but also provided numerous essential features for request handling and linking to the HTML pages.
SQLite was used for the database itself, as it integrates easily with Python, which simplified the development process of the application.
Flask-SQLAlchemy was also used to simplify the interaction between Flask, Python, and SQLite.
HTML was used to provide the user with the visual aspect of the database and the exercise summary.
Jinja2 was used as it helped to link up Flask and the HTML templates used with this application.

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [Stack Overflow](https://stackoverflow.com/)
- [GitHub](http:www.github.com/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Full Stack Python - Flask](https://www.fullstackpython.com/flask.html/)
- [YouTube](http:www.youtube.com/)
- [Geeks for Geeks](https://www.geeksforgeeks.org/flask-tutorial/)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}

1. Enchance and improve upon the user interface.
2. Add more error handling.
3. Have somewhere where users can report bugs/issues.
4. Improve security within the code.
5. Introduce a notification/reminder system.
6. Consider using external APIs.
7. Add more visual things to the data, such as graphs/charts.