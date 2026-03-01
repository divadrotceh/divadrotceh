from flask import Blueprint, Response, make_response, request, redirect, session, render_template
import jwt
from hashlib import sha1
from db import db_controller as db_cont
from app import app
from uuid import uuid4

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    session["username"] = username
    if not username or not password:
        return make_response({"message": "please enter credentials"}, 401)
    
    requested = db_cont.select_one("users", "name", username)

    if not requested:
        return redirect("/auth/logon")
    
    if sha1(password.encode()).hexdigest() != requested["hashed_password"]:
        return Response(status=401)

    token = jwt.encode({"username": username}, key=app.secret_key)
    session["token"] = token

    resp = make_response({"session":session}, 200)
    resp.set_cookie("some_cookie","123")
    return redirect("/index/tasks", 302, resp)


#curl -X POST -H "Content-Type: application/json" -d '{"username": "david", "password":"1234"}' http://127.0.0.1:5000/auth/signup
@bp.route("/signup", methods = ["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    username = request.form.get("username")
    password = request.form.get("password")
    
    if db_cont.select_one("users", "name", username):
        return make_response("User already in use", 409)

    new_user = {
        "id": uuid4().hex,
        "name": username,
        "hashed_password": sha1(password.encode()).hexdigest()
    }


    db_cont.insert_value("users", new_user)
    
    token = jwt.encode({"username": username}, key=app.secret_key)
    session["token"] = token

    resp = make_response({"session":session}, 200)
    return redirect("/index/tasks", 302, resp)

@bp.route("/test", methods= ["GET", "POST"])
def tests():
    data = request.form.get("username")
    if request.method == "POST":
        return make_response(data)

@bp.route("/logout")
def logout():
    session.clear()
    resp = make_response("Logout successful", 200)
    resp.delete_cookie("some_cookie")
    return redirect("/index/home")
