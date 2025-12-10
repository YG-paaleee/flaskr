from flask import Blueprint

indexBp = Blueprint("index", __name__)

@indexBp.route("/")
def health():
    return "ralph angelo badang setup"