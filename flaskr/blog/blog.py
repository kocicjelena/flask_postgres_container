
from flask import (Blueprint, g, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from sqlalchemy import desc
from werkzeug.exceptions import abort
from flaskr.models import DB
from flaskr.models.models import Blog, User
from sqlalchemy.exc import IntegrityError
from flaskr.auth.auth import login_required
#from flaskr.db import get_db
from uuid import uuid4
from flaskr.database import db_session
bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    posts = Blog.query.all()
    #posts = Blog.query.filter(Blog.author_id == User.id).all()
    #posts = Blog.query.filter(Blog.author_id == User.id).order_by(desc(Blog.created)).all()
    #posts = DB.query(Blog).filter(Blog.author_id == User.id).order_by(desc(Blog.created)).all()

    # db = get_db()
    # posts = db.execute(
    #     "SELECT p.id, title, body, created, author_id, username"
    #     " FROM post p JOIN user u ON p.author_id = u.id"
    #     " ORDER BY created DESC"
    # ).fetchall()
    return render_template("blog/index.html", posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = Blog.query.get(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != User.id:
        abort(403)

    return post


# @bp.route("/create", methods=("GET", "POST"))
# @login_required
# def create():
#     """Create a new post for the current user."""
#     if request.method == "POST":
#         title = request.form["title"]
#         body = request.form["body"]
#         error = None

#         if not title:
#             error = "Title is required."
#         if User.id is None:
#             error = 'user doesnot exist'
#         if error is not None:
#             flash(error)
#         else:
#             bl = Blog(id=uuid4(),
#                 title=title,
#                 body=body,
#                 author_id=User.id)
#             db_session.add(bl)
#             db_session.commit()
#             return redirect(url_for("blog.index"))

#     return render_template("blog/create.html")

    # sqlite:

    #     if not title:
    #         error = "Title is required."

    #     if error is not None:
    #         flash(error)
    #     else:
    #         db = get_db()
    #         db.execute(
    #             "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
    #             (title, body, g.user["id"]),
    #         )
    #         db.commit()
    #         return redirect(url_for("blog.index"))

    # return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db_session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


    # lite
    # post = get_post(id)

    # if request.method == "POST":
    #     title = request.form["title"]
    #     body = request.form["body"]
    #     error = None

    #     if not title:
    #         error = "Title is required."

    #     if error is not None:
    #         flash(error)
    #     else:
    #         db = get_db()
    #         db.execute(
    #             "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
    #         )
    #         db.commit()
    #         return redirect(url_for("blog.index"))

    # return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = get_post(id)
    db_session.delete(post)
    db_session.commit()
    return redirect(url_for("blog.index"))
