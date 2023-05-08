import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from flaskr.models import DB, Blog, User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from uuid import uuid4
from sqlalchemy.orm import scoped_session, sessionmaker
from typing import Generator
# sqlite:
# from flaskr.db import get_db
from flaskr.database import db_session, get_sess
bp = Blueprint("auth", __name__)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if User is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
@login_required
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    #user_id = User.query.filter(User.id=='user_id').first()
    #User = None
    sess = get_sess()
    
    db_session.query
    #with Session(e) as sess:
    if User is not None:
        db_session.query(User).filter(User.id=='user_id').first()


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # sqlite:
        # db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            user = User.query.filter(user.username==username).first()
            if user:
                flash('username address already exists')
                return redirect(url_for('auth.register'))
            
            # We can avoid IntergrityError using uuid4.
            new_user = User(id=uuid4(),
                            username=username,
                            password=generate_password_hash(password, method='sha256'))
            
            db_session.add(new_user)
            db_session.commit()

        # code for sqlite:
        #     try:
        #         db.execute(
        #             "INSERT INTO user (username, password) VALUES (?, ?)",
        #             (username, generate_password_hash(password)),
        #         )
        #         db.commit()
        #     except db.IntegrityError:
        #         # The username was already taken, which caused the
        #         # commit to fail. Show a validation error.
        #         error = f"User {username} is already registered."
        #     else:
        #         # Success, go to the login page.
        #         return redirect(url_for("auth.login"))

        # flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        
        password = request.form["password"]
        # password = request.form.get('password')

        user = User.query.filter(User.username==username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for('index'))

        flash(error)

        # sqlite:
        # db = get_db()
        # error = None
        # user = db.execute(
        #     "SELECT * FROM user WHERE username = ?", (username,)
        # ).fetchone()

        # if user is None:
        #     error = "Incorrect username."
        # elif not check_password_hash(user["password"], password):
        #     error = "Incorrect password."

        # if error is None:
        #     # store the user id in a new session and return to the index
        #     session.clear()
        #     session["user_id"] = user["id"]
        #     return redirect(url_for("index"))

        # flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
