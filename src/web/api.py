import os
from flask import Flask, request
from src import config
import logging
import logging.config


def create_app(test_config=None):
    from src.web.views import views_blueprint

    app = Flask(__name__)
    app.config.from_object(test_config or os.environ["APP_SETTINGS"])
    logging.config.dictConfig(app.config["LOGGING"])
    log = logging.getLogger(__name__)
    log.info("starting web api")
    app.register_blueprint(views_blueprint)
    return app


def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))

    create_app().run(host=host, port=port)


if __name__ == "__main__":
    main()
