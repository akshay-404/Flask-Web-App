# 🔐 Flask Authentication App

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-2.x-black)](https://flask.palletsprojects.com/)  
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)](https://www.sqlalchemy.org/)  
[![AWS](https://img.shields.io/badge/AWS-EC2-orange)](https://aws.amazon.com/ec2/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  

A simple **Python Flask web application** with user authentication.  
Users can **create an account** and **log in**. User credentials are securely stored in a database using **hashed passwords**.  

The app is designed to run locally (e.g., on WSL in Windows 11) and later be deployed on an **AWS EC2 instance** with Apache2.  

---

## 🚀 Features
- User signup and login functionality
- Passwords stored in **hashed format** (using Werkzeug)
- SQLite for local development (can be swapped with AWS RDS in production)
- Integration-ready with **Apache2 / mod_wsgi**
- Clean **HTML + CSS templates**
- Flash messages for success/error feedback

---

## 📂 Project Structure

auth_app/
├── app.py                  # Main Flask application (routes + logic)
├── config.py               # Configuration settings (DB URL, secret keys, env variables)
├── models.py               # SQLAlchemy models (User, KeyValue)
├── wsgi.py                 # Entry point for Apache2 + WSGI
│
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (NOT in GitHub)
├── .gitignore              # Ignore venv, db, cache files
│
├── instance/
│   └── auth_app.db         # SQLite database (local dev only, ignored in Git)
│
├── static/
│   └── css/
│       └── style.css       # Styling for templates
│       └── favicon.ico     # Icon for the web app
│
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   ├── login.html          # Login page
│   ├── register.html       # User registration page
│   └── dashboard.html      # Dashboard after login
│
├── deploy/
│   └── apache/
│       └── auth_app.conf   # Apache2 virtual host config
│
└── README.md               # Project documentation


