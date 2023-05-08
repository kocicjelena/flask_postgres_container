import click
from flask.cli import with_appcontext

from flaskr.models import DB, User, Blog

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    click.echo('Creating all the tables...')
    DB.create_all()