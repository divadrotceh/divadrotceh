from hashlib import sha1
from flask import Blueprint, request, make_response, redirect, Response, session, render_template
import jwt
from functools import wraps
from app import app
from datetime import datetime
from uuid import uuid4
from db import db_controller as db_cont

bp = Blueprint("views",__name__, url_prefix="/index")
superUser = {
    "user": "divadrotceh",
    "password": "1234"
}
#decorator
def super_user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return make_response({"message": "No credentials added"}, 401)
        
        if auth.username == superUser["user"] and auth.password == superUser["password"]:
            return func(*args, **kwargs)
        else:
            return make_response({"message": "Wrong credentials"}, 401)
    return wrapper

#decorator
def auth_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        auth = request.authorization

        if not auth:
            return redirect("/auth/login")

        
        username = auth.username
        password = auth.password
        token = auth.token

        if username and password:
            requested = db_cont.select_one("users", 'name', username)
    
            if not requested:
                return redirect("/auth/signup")
            
            if requested.get("hashed_password") != sha1(password.encode()).hexdigest():
                return make_response({"message":"Invalid Credentials"}, 401)
            else:
                return func(*args, **kwargs)

        else:
            try:
                payload = jwt.decode(token, key=app.secret_key, algorithms="HS256")
                username = payload["username"]
                if db_cont.select_one("users", "name", username):
                    auth.username = username
            except jwt.exceptions.DecodeError:
                return make_response({"message": "wrong token"}, 401)
        return func(*args,**kwargs)
    return wrapper

def session_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect("/auth/login")
        try:
            if "token" not in session:
                return redirect("/auth/login")
            payload = jwt.decode(session["token"], app.secret_key, "HS256")
            if session["username"] != payload["username"]:
                return redirect("/auth/login")
        except jwt.exceptions.DecodeError:
            return make_response({"message": "wrong token"}, 401)
        return func(*args, **kwargs)
        
    return wrapper

@bp.get("/home")
def home_page():
    return render_template("home.html")

#Testing Token curl -X GET http://127.0.0.1:5000/index/tasks -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImhlY3RvciJ9.BdeZay3pAlpz18SjaB2mt0bonFdxxOWwE4evrLc6g0o"
@bp.get("/tasks")
@session_required
def get_lists():
    user_tasks = db_cont.select_all("tasks", "username", session["username"])
    return render_template("tasks.html", tasks = user_tasks)
#("id", "name", "is_completed", "created_at", "username",)

@bp.post("/tasks")
@session_required
def create_task():
    fields = {
        "id": uuid4().hex,
        "name": request.form.get("name", "No name specified"),
        "is_completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": session["username"]
    }
    db_cont.insert_value("tasks", fields)
    return redirect("/index/tasks")

@bp.put("/tasks/<task_id>")
@session_required
def update_task(task_id):
    body = request.json
    db_cont.edit_by_id("tasks", body, task_id)
    task = db_cont.select_one("tasks", "id", task_id)
    if not task:
        return make_response({"message":"Task not Found"},404)
    return make_response(task)

#curl -X GET http://127.0.0.1:5000/index/get_users -u "divadrotceh:1234"
@bp.get("/get_users")
@super_user_required
def get_users():
    users = db_cont.show_all("users")
    return make_response(users)

#curl -X GET http://127.0.0.1:5000/index/test -u "divadrotceh:1234"
@bp.get("/test")
@session_required
def testing():
    return make_response({"cookies":request.cookies.get("some_cookie")}, 200)

