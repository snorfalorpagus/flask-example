from flask import Blueprint, request
from jinja2 import Environment

blueprint = Blueprint("hello", __name__)

env = Environment()


@blueprint.route("/")
def hello():
    name = request.args.get("name", "World")
    template = env.from_string("Hello, {{ name | e }}!")
    return template.render(name=name)
