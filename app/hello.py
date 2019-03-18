from flask import Blueprint, request

blueprint = Blueprint("hello", __name__)


@blueprint.route("/")
def hello():
    name = request.args.get("name", "World")
    return f"Hello, {name}!"
