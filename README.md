*Look for the bare necessities  
The simple bare necessities  
Forget about your worries and your strife  
I mean the bare necessities  
Old Mother Nature's recipes  
That brings the bare necessities of life*

# Bare Necessities

A minimalist web application for Mozilla cloud services that does 99% of what you'll need to run stuff in prod.


It implements [Dockerflow](https://github.com/mozilla-services/Dockerflow/).  
Requires Python 3.8 with [Black formatting](https://black.readthedocs.io/en/stable/), [mypy type checking](https://mypy.readthedocs.io/en/stable/), etc.
Uses [Flask](https://flask.palletsprojects.com/en/1.1.x/) for the web side.  
[Celery](http://docs.celeryproject.org/en/latest/index.html) for the worker side.  
[SQLAlchemy & PostgreSQL](https://docs.sqlalchemy.org/en/13/dialects/postgresql.html) for the data side.  

## Development

Setup a virtualenv with
```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements/defaults.txt -r requirements/dev.txt
```

You can then run the development server using `gunicorn --reload --chdir src src.web.wsgi:app`