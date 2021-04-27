from os import spawnl
import sqlite3
import json
from models import User

def register_new_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        INSERT INTO users
            ('first_name', 'last_name', 'email', 'bio', 'username', 'password', 'created_on')
        VALUES
            (?,?,?,?,?,?,?)
        """, (new_user["firstName"], 
                new_user["lastName"], 
                new_user["email"], 
                new_user["bio"], 
                new_user["username"], 
                new_user["password"], 
                new_user["createdOn"],
        ))

        id = db_cursor.lastrowid

        new_user["id"] = id

        return json.dumps(new_user)

