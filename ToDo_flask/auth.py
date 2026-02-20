from flask import Blueprint, Response, make_response, request

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods = ["GET", "POST"])
def login():
    auth = request.authorization
