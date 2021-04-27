import sqlite3
import json
from models import User

def register_new_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor() 

        db_cursor.execute(""" 
        INSERT INTO users
            ('first_name', 'last_name', 'display_name' 'email', 'bio', 'username', 'password', 'created_on', 'profile_image_url', 'is_admin')
        VALUES
            (?,?,?,?,?,?,?, ?)
        """, (new_user["firstName"], 
                new_user["lastName"],
                new_user["displayName"], 
                new_user["email"], 
                new_user["bio"], 
                new_user["username"], 
                new_user["password"], 
                new_user["createdOn"],
                new_user["profileImagUrl"],
                new_user["isAdmin"]
        ))

        id = db_cursor.lastrowid

        new_user["id"] = id

        return json.dumps(new_user)

def existing_user_check(login_info):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            u.id
        FROM users u
        WHERE u.username = ? and u.password = ?
        """, (login_info["username"], login_info["password"]))

        data = db_cursor.fetchone()

        response = {}

        if data["id"]:
            response = {
                "valid": "valid",
                "token": data["id"]
            }

        return json.dumps(response)

def get_all_users():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT 
            u.first_name,
            u.last_name,
            u.display_name,
            u.is_admin
        FROM users u
        """)

        dataset = db_cursor.fetchall()

        users = []

        for row in dataset:
            user = User(first_name = row["first_name"], 
                        last_name = row["last_name"], 
                        display_name = row["display_name"], 
                        user_name = None, 
                        password = None,
                        email = None, 
                        bio = None, 
                        created_on = None, 
                        is_admin = row["is_admin"])

            users.append(user.__dict__)

        return json.dumps(users)







