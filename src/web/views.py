from flask import abort, Blueprint, Response, request, send_from_directory

views_blueprint = app = Blueprint("views_blueprint", __name__)


@app.route("/")
def hello():
    return "Hello World!"
