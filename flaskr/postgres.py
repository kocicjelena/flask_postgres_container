import sqlite3
from typing import Generator

import click
from flask import current_app
from flask import g

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

db_conf = CON.db.postgres
connection_url = (f'postgresql+psycopg2://{db_conf.POSTGRES_USER}'
                  f':{db_conf.POSTGRES_PASSWORD}@{db_conf.host}'
                  f'/{db_conf.POSTGRES_DB}')
db = create_engine(connection_url)

Base = declarative_base()


db_session = scoped_session(sessionmaker(bind=db))
Base.query = db_session.query_property()

#@lru_cache
def create_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
    # SessionLocal =db_session()
    return SessionLocal

def generator_session() -> Generator:
    Session = create_session()
    with Session() as session:
        try:
            yield session
        finally:
            session.close()

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # if "db" not in g:
    #     g.db = sqlite3.connect(
    #         current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    #     )
    #     g.db.row_factory = sqlite3.Row

    # return g.db


# def close_db(e=None):
#     """If this request connected to the database, close the
#     connection.
#     """
#     db = g.pop("db", None)

#     if db is not None:
#         db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    db.connect()
    # with current_app.open_resource("schema.sql") as f:
    #     db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
