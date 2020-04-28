from flask import abort, Blueprint, Response, request, send_from_directory
import logging

log = logging.getLogger("web.api")

views_blueprint = app = Blueprint("views_blueprint", __name__)


@app.route("/", methods=["GET"])
def hello():
    log.info("someone said hello")
    return "Hello World!"


@app.route("/<name>", methods=["GET"])
def hello_name(input_name):
    log.info(f"{input_name} said hello", extra={"input_name": name})
    return f"Hello {name}"
