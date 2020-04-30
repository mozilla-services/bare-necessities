*Look for the bare necessities  
The simple bare necessities  
Forget about your worries and your strife  
I mean the bare necessities  
Old Mother Nature's recipes  
That brings the bare necessities of life*

# Bare Necessities

A minimalist web application for Mozilla cloud services that does 99% of what you'll need to run stuff in prod.


It implements [Dockerflow](https://github.com/mozilla-services/Dockerflow/) using the excellent [python-dockerflow](https://python-dockerflow.readthedocs.io/).  
Requires Python 3.8 with [Black formatting](https://black.readthedocs.io/en/stable/), [mypy type checking](https://mypy.readthedocs.io/en/stable/), etc.  
Uses [Flask](https://flask.palletsprojects.com/en/1.1.x/) for the web side.  
[Celery](http://docs.celeryproject.org/en/latest/index.html) for the worker side.  
[SQLAlchemy & PostgreSQL](https://docs.sqlalchemy.org/en/13/dialects/postgresql.html) for the data side.  

## Development

For local development, setup a virtualenv with
```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements/defaults.txt -r requirements/dev.txt
```

You can then run the development server using `gunicorn --reload --chdir src src.web.wsgi:app`

If you want a full stack, with database, workers and so on, use `docker-compose up --build`.

## Heroku

Use your SSO account to [log into heroku](https://sso.mozilla.com/heroku) and verify that you have access to it. (and it not, [follow this doc](https://mana.mozilla.org/wiki/display/TS/Using+SSO+with+your+Heroku+account))

Then from the command line:

``` bash
heroku login
heroku create $(whoami)-barenecessities-$(date +%s)
git push heroku master
```

Deployment to heroku is also automated from circleci using a dedicated service account and a non-expiring API key. The documentation on how to get one of these [is on mana](https://mana.mozilla.org/wiki/display/TS/Obtaining+non-expiring+API+keys).

## How does it work?

Bare-necessities is a cloud service composed of a web api, a database and an asynchronous worker. The web api and the worker talk to each other via tasks that transit through the database.

The API exposes its endpoints in `src/web/views.py`. You can add and remove endpoints from that file directly, or add more from another file.

### standard http endpoints

The [Dockerflow](https://github.com/mozilla-services/Dockerflow/) standard requires web apis to expose several endpoints: **__version**, **__heartbeat__** and **__lbheartbeat__**. Those endpoints are meant to be used by the infrastructure to help operate production services. In this application, the standard http endpoints are transparently enabled by the **python-dockerflow** package, so you won't find them in `src/web/views.py`.

### logging

All applications must log to standard output in the [JSON mozlog format](https://wiki.mozilla.org/Firefox/Services/Logging). Bare-necessities implements this using the [python-dockerflow](https://python-dockerflow.readthedocs.io/en/latest/logging.html) package, in two different ways:

1. Request logging is configured in `src/web/api.py` to log every request summary using mozlog. (the `request.summary` logger in `src/config.py`)
2. Application logging is done by obtaining a logger via `log = logging.getLogger("web.api")` and simply logging with `log.info("my log message")`. You can also pass a dictionary of fields to the `extra` parameters of the `log.info` call, like so `log.info("hello", extra={"world": name})`. For examples, see `src/web/views.py`.

### docker setup

The standard dockerflow process to deploy a service to production is to package the application into a docker container and upload that container to hub.docker.com. The [Mozilla's organization on hub.docker.com](https://hub.docker.com/u/mozilla) lists all the applications being hosted there.

Building and uploading an application container must be done in CI, typically circleci or taskcluster, such that it doesn't depend on any particular individual running the task by hand.

The `Dockerfile` at the root of the repository is used to package the application. That Dockerfile is referenced by **docker-compose** in its configuration `docker-compose.yml`, as follows:

```yaml
  web:
    container_name: bare-necessities
    build:
        context: .
    image: mozilla/bare-necessities
```

Here, `build.context: .` means the `Dockerfile` is located in the same folder as the `docker-compose.yml` file. In the circleci configuration at `.circleci/config.yml`, the task `build-images` will then create the docker images by calling `docker-compose build`.

In order to upload containers, you'll need to ask cloudops to create the dockerhub repository for you. They'll give you back credentials to put in the DOCKERHUB_REPO, DOCKER_USER and DOCKER_PASS environment variables of circleci. Then, the circleci task `upload-docker-images` takes care of publishing images to dockerhub.

## database

The postgres database is managed by the application through SQLAlchemy. The tables are defined under `src/db/models` as classes that inherit the `db.Model` class.

### sqlite

For local development and testing, it is possible to use sqlite instead of postgresql.

To create a sqlite local database under `/tmp/bare_necessities.sqlite`, use the following command:

```
$ SQLALCHEMY_DATABASE_URI=sqlite:////tmp/bare_necessities.sqlite \
  PYTHONPATH=. \
  FLASK_APP=src/web/api.py \
  flask db upgrade
```

You can then start the web api using this command:

```
$ SQLALCHEMY_DATABASE_URI=sqlite:////tmp/bare_necessities.sqlite \
  PYTHONPATH=. \
  FLASK_APP=src/web/api.py \
  gunicorn --chdir src --reload src.web.wsgi:app
```

The api will be listening on `127.0.0.1:8000`.

### database migrations

The database schema is entirely managed by flask via the alembic package. Changes to running databases are applied as migration that can be upgraded and downgraded as needed.

*Note: this section is convoluted due to the way docker-compose work. Ideally, these commands would run in the `web` container, but because its volume is read-only, flask can't write migration files. Therefore, we run the flask commands locally by pointing at the running `db` container.*

First, spin up a stack in docker-compose. The database instance will be instanciated without any table.

```
$ docker-compose up --build
```

Then, retrieve the IP address of the `db` container.

```
$ export DBIP=$(docker inspect bare-necessities-db| jq -r '.[].NetworkSettings.Networks.barenecessities_default.IPAddress')
```

Run the `flask db init` command against the `db` container. This will create a local folder named `migrations` with all the boilerplate needed to handle schema migrations.

```
$ SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@${DBIP}:5432/bare_necessities \
  PYTHONPATH=. \
  FLASK_APP=src/web/api.py \
  flask db init
```

Run the `flask db migrate` command to create the initial schema version. This will create a file under `migrations/versions` with the initial schema of the database.

```
$ SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@${DBIP}:5432/bare_necessities \
  PYTHONPATH=. \
  FLASK_APP=src/web/api.py \
  flask db migrate -m "Initial migration."
```

Finally, to apply this schema to the database and create the tables, run the `flask db upgrade` command.

```
$ SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@${DBIP}:5432/bare_necessities \
  PYTHONPATH=. \
  FLASK_APP=src/web/api.py \
  flask db upgrade
```

We can verify that the tables have been created in the database. The `alembic_version` table contains the version number that maps to the schema version currently applied. You will find a corresponding migration version file under `migrations/versions`.

```
$ psql -U postgres -h ${DBIP} bare_necessities

bare_necessities=# \d+
                             List of relations
 Schema |      Name       |   Type   |  Owner   |    Size    | Description 
--------+-----------------+----------+----------+------------+-------------
 public | alembic_version | table    | postgres | 8192 bytes | 
 public | user            | table    | postgres | 8192 bytes | 
 public | user_id_seq     | sequence | postgres | 8192 bytes | 
(3 rows)

bare_necessities=# select * from alembic_version;
 version_num  
--------------
 ddb81cb8c19f
(1 row)
```
