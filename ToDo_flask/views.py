from hashlib import sha1
from flask import Blueprint, request, make_response, redirect, Response
from db import users, tasks
import jwt
from functools import wraps
from app import app
from datetime import datetime
from uuid import uuid4

bp = Blueprint("tasks",import_name=__name__,url_prefix="")
superUser = {
    "user": "divadrotceh",
    "password": 1234
}

def super_user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization

        if auth.username == superUser["user"] and auth.password == superUser["password"]:
            return func(*args, **kwargs)
        
        else:
            Response(status=401)
    
    return wrapper

def auth_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        auth = request.authorization
        if not auth:
            return redirect("/login")
        if auth.username not in users:
            return redirect("/logon")

        if users[auth.username] != sha1(auth.password.encode()).digest():
            return Response(status=401)

        if auth.token != jwt.encode({"username": auth.username}, app.secret_key):
            return redirect("/login")
        
        return func(*args, **kwargs)

    return wrapper

@bp.get("/")
@auth_required
def get_lists():
    auth = request.authorization
    user_tasks = {
        task: fields for task, fields in tasks.items() if 
        fields["username"] == auth.username
    }
    return make_response(user_tasks)

bp.post("/")
@auth_required
def create_task():
    fields = {
        "name": request.json.get("name", "No name specified"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_completed": False,
        "username": request.authorization.username
    }
    _id = uuid4().hex
    tasks[_id] = fields
    return make_response({"Task ID": _id})

bp.get("/users")
@super_user_required
def get_users():
    return make_response(users)
