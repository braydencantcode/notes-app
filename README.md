Full-stack notes app with user accounts, built with Flask and SQLite

Features:
user sign up / log in with session authentication
isolated and private notes for each user
notes persist across sessions, and stored on SQLite database
case insensitive usernames
add and clear notes (via HTTP requests GET, DELETE, and POST)
dark mode toggle

Tech stack:
Back end: Python, Flask
Front end: HTML, CSS, JavaScript
Database: SQLite

What I learned:
This is my first "full stack" project. I learned how to use Flask and app routes to map a URL to a Python function on the back end. I learned how to query SQLite within a Python program to retrieve data. I learned how the front end and back end communicate via HTTP requests and JSON. 

Next steps:
Password hashing (currently stored in plain text...)
Account deletion system
Password reset system
Note encryption
