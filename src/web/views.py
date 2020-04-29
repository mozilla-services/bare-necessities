from src.db import models
from flask import abort, Blueprint, Response, request, send_from_directory
import logging

log = logging.getLogger("web.api")

views_blueprint = app = Blueprint("views_blueprint", __name__)


@app.route("/", methods=["GET"])
def hello():
    log.info("someone said hello")
    return "Hello World!"


@app.route("/<input_name>", methods=["GET"])
def hello_name(input_name):
    log.info(f"{input_name} said hello", extra={"input_name": input_name})
    return f"Hello {input_name}"


@app.route("/user/<input_name>", methods=["GET"])
def get_user_details(input_name):
    log.info(f"retrieving user details", extra={"input_name": input_name})
    return models.get_user_details(input_name)


@app.route("/user/<input_name>", methods=["POST"])
def user_details(input_name):
    log.info(f"retrieving user details", extra={"input_name": input_name})

    return f"Hello {input_name}"
