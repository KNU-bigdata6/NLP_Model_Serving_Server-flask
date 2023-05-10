@echo off
IF NOT EXIST venv (
  python -m venv venv
  venv\scripts\activate
  pip install --upgrade pip
  pip install -r requirements.txt
)

SET FLASK_APP=app.py
SET FLASK_RUN_PORT=8000
flask run
