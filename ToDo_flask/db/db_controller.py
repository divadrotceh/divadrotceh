import sqlite3, os
from pathlib import Path
from functools import wraps

main_path = Path(__file__).resolve().parent
storage = os.path.join(main_path, "storage")

allowed_tables = ("users", "tasks")
allowed_columns = {
    "users": ("id", "name", "hashed_password"),
    "tasks": ("id", "name", "is_completed", "created_at", "username",),
}

execute_sql_script = {
    "users": """
            CREATE TABLE if not exists users
                    (id VARCHAR(32) primary key,
                    name VARCHAR(50),
                    hashed_password VARCHAR(50));
        """,
    "tasks": """
            CREATE TABLE if not exists tasks
                    (id VARCHAR(32) primary key,
                    name VARCHAR(50),
                    is_completed BOOLEAN,
                    created_at DATETIME,
                    username VARCHAR(50))
            """
}

def validate_table(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args: table_name = args[0]
        else: table_name = kwargs["table_name"]
        if table_name not in allowed_tables:
            raise Exception("Non existing table.")
        return func(*args, **kwargs)
    return wrapper

def validate_columns(table_name, table):
    for key in table.keys():
        if key not in allowed_columns[table_name]:
            raise Exception(f"{key} Column not in table")
    return 0

@validate_table
def create_table(table_name):
    """
    Docstring for create_table
    
    :param file_name: Description
    the sqlite3.connec() as file manager implements the __exit()__
    magic method with the con.commit() and con.close().
    So we don't need to call them manually every time.
    """
    file_name = table_name + ".db"
    db_file = os.path.join(storage,file_name)
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        cur.execute(execute_sql_script[table_name])

@validate_table
def insert_value(table_name, values={}):
    file_name = table_name + ".db"
    db_file = os.path.join(storage,file_name)
    validate_columns(table_name, values)
    columns = ",".join(values.keys())
    placeholders = ','.join('?' for _ in values.keys())
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cur.execute(query, tuple(values.values()))

@validate_table
def select_one(table_name, attribute, value):
    file_name = table_name + ".db"
    db_file = os.path.join(storage, file_name)
    validate_columns(table_name, {attribute:value})
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {attribute} = ?", (value,))
        element = cur.fetchone()
    if element is None:
        return {}
    return dict(zip(allowed_columns[table_name], element))

@validate_table    
def select_all(table_name, attribute, value):
    file_name = table_name + ".db"
    db_file = os.path.join(storage, file_name)
    validate_columns(table_name, {attribute:value})
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {attribute} = ?", (value, ))
        res = cur.fetchall()
    if not res:
        return []
    ret = [dict(zip(allowed_columns[table_name], entry)) for entry in res]
    return ret

@validate_table    
def show_all(table_name):
    file_name = table_name + ".db"
    db_file = os.path.join(storage, file_name)
    res = ""
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        res = cur.fetchall()
    return res

#UPDATE {table_name} SET {set_clause} WHERE id = ?
@validate_table
def edit_by_id(table_name, values={}, id=""):
    file_name = table_name + ".db"
    db_file = os.path.join(storage, file_name)
    validate_columns(table_name,values)

    set_clause = ",".join([key + " = ?" for key in values.keys()])
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        cur.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", (tuple(values.values()) + (id,)))

if __name__ == "__main__":
    table_name = "tasks"
    create_table(table_name)
    table_name = "users"
    create_table(table_name)