from flask import abort, Blueprint, Response, request, send_from_directory

views_blueprint = app = Blueprint("views_blueprint", __name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World!"


@app.route("/<name>", methods=["GET"])
def hello_name(name):
    return f"Hello {name}"
