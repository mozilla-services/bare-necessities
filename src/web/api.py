import os
from flask import Flask, request
from flask_migrate import Migrate
import logging
import logging.config
from dockerflow.flask import Dockerflow
from dockerflow.logging import JsonLogFormatter
from src.web.views import views_blueprint
import src.db.models as models
from src import config

# silence flask request logging
flasklog = logging.getLogger("werkzeug")
flasklog.setLevel(logging.ERROR)

# override the summary logger from the Dockerflow class to add
# logging of query string
# https://github.com/mozilla-services/python-dockerflow/issues/44
class Customflow(Dockerflow):
    def summary_extra(self):
        out = super().summary_extra()
        out["query_string"] = request.query_string.decode("utf-8")
        return out


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("src.config")

    logging.config.dictConfig(app.config["LOGGING"])
    log = logging.getLogger("web.api")
    log.info("starting web api")

    log.info(f"connecting to database")
    models.db.init_app(app)
    migrate = Migrate(app, models.db)

    dockerflow = Customflow(app, db=models.db, migrate=migrate)
    dockerflow.init_app(app)

    app.register_blueprint(views_blueprint)

    return app


if __name__ == "__main__":
    create_app().run()
