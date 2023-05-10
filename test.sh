#!/bin/bash
chmod 755 ./runserver.py

if [ ! -d venv ]; then
	python3 -m venv venv
	source venv/bin/activate
	pip install --upgrade pip
	pip install -r requirements.txt
fi
export FLASK_APP=app.py
export FLASK_RUN_PORT=8000
flask run

