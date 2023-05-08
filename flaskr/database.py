from typing import Generator
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI="postgresql+psycopg2://jelena:jelena@psql/jelena_db"

engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import flaskr.models
    Base.metadata.create_all(bind=engine)
    
#@lru_cache
def create_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # SessionLocal =db_session()
    return SessionLocal

def generator_session() -> Generator:
    Session = create_session()
    with Session() as session:
        try:
            yield session
        finally:
            session.close()
def get_sess():
    generator_session()


def close_db(e=None):
    db_session.remove()
    
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
