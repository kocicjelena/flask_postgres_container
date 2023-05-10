flask

docker-compose build
docker-compose up

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat



Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
 

 TODO: make alembic
 
 helpfull resources:
 https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.htmlhttps://flask.palletsprojects.com/en/2.3.x/patterns/sqlalchemy/
 https://copyprogramming.com/howto/trying-to-pass-two-parameters-from-an-html-form-in-flask-in-url-to-then-run-in-a-python-program
 https://www.programcreek.com/python/example/50108/werkzeug.exceptions.NotFound
 https://community.plotly.com/t/forcing-dash-app-to-be-called-through-flask-route/25833/3
 https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
 