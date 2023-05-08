import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.commands import create_tables
from flaskr.database import init_app
from flaskr.models import DB
from sqlalchemy import create_engine
from flaskr.database import db_session

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app.config['SECRET_KEY'] = 'SECRET_KEY'
    # app.config["SQLALCHEMY_ECHO"] = True
    # app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.update(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    #from flaskr import db
    #DB = SQLAlchemy(app)
    #DB.init_app(app)
    #DB.create_all()
   
    #initiate_db(app)
    # @app.before_request
    # def create_database():
    #         DB.create_all()
            #app.cli.add_command(create_tables)
    with app.app_context():
      try:
              init_app(app)
              #app.cli.add_command(create_tables)
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))
      finally:
          print("db.create_all() in __init__.py was successfull - no exceptions were raised")
          #from .models import User

    #db.init_app(app)

    # apply the blueprints to the app
    #from flaskr import auth, blog
    from flaskr.auth import auth
    from flaskr.blog import blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    #app.add_url_rule("/", endpoint="index")
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    return app
def initiate_db(app):
    DB.init_app(app=app)
