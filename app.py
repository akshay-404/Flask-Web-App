from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import User, UserKV
from passlib.hash import argon2
from functools import wraps

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

app = create_app()
db = SQLAlchemy(app)

# Forms
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Re-enter Password", validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = db.session.query(User).filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash("Username or email already exists.", "error")
            return render_template("register.html", form=form)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=argon2.hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user and argon2.verify(form.password.data, user.password_hash):
            session["user_id"] = user.id
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    user = db.session.query(User).get(session["user_id"])
    if user is None:
        flash("User not found.", "error")
        return redirect(url_for("logout"))
    kvs = db.session.query(UserKV).filter_by(user_id=user.id).all()
    return render_template("dashboard.html", user=user, kvs=kvs)

@app.route("/kv", methods=["POST"])
@login_required
def add_kv():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    if not key or not value:
        flash("Both key and value are required.", "error")
        return redirect(url_for("dashboard"))
    kv = UserKV(user_id=session["user_id"], k=key, v_hash=argon2.hash(value))
    db.session.add(kv)
    db.session.commit()
    flash("Key/Value stored (value hashed)", "success")
    return redirect(url_for("dashboard"))

@app.context_processor
def inject_db_and_models():
    from models import User
    return dict(db=db, models=__import__('models'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
