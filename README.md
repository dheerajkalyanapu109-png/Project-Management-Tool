# Project Management Tool

A collaborative Trello/Asana-style tool built with Django, Django Channels (WebSockets), SQLite, HTML, CSS and JavaScript.

## Features
- Register, log in, log out
- Create group projects and add members by username
- Project board with To do / In progress / Done columns and task cards
- Create tasks, assign them to members, move them between columns
- Comment on tasks
- **Bonus:** notifications (assigned, commented, added to project) and real-time board/comment updates over WebSockets

## Database tables
users (Django auth), Project (with members), Task, Comment, Notification

## Run locally
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations tracker
    python manage.py migrate
    python manage.py seed              # demo users alice and bob, password demo12345
    python manage.py runserver

Open http://127.0.0.1:8000. To see real-time updates, log in as `alice` in one window and `bob` in a private window, open the same project, and change a task.
