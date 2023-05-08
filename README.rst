

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat

Install Flaskr::

    $ pip install -e .


    $ flask --app flaskr init-db
    $ flask --app flaskr run --debug


Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
 RuntimeError: The current Flask app is not registered with this 'SQLAlchemy' instance. Did you forget to call 'init_app', 
 or did you create multiple 'SQLAlchemy' instances?
 https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#configuration

 AttributeError: 'NoneType' object has no attribute 'query'
 https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html