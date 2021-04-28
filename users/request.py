import sqlite3
import json
from models import User

def register_new_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor() 

        # Create class instance before insert

        db_cursor.execute(""" 
        INSERT INTO users
            ('first_name', 'last_name', 'display_name' 'email', 'bio', 'username', 'password', 'created_on', 'profile_image_url')
        VALUES
            (?,?,?,?,?,?,?)
        """, (new_user["firstName"], 
                new_user["lastName"],
                new_user["displayName"], 
                new_user["email"], 
                new_user["bio"], 
                new_user["username"], 
                new_user["password"], 
                new_user["createdOn"],
                new_user["profileImageUrl"]
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
            u.id,
            u.active
        FROM users u
        WHERE u.username = ? and u.password = ?
        """, (login_info["username"], login_info["password"]))

        data = db_cursor.fetchone()

        response = {}

        if data:
            if data["active"]:
                response = {
                    "valid": "valid",
                    "token": data["id"]
                }
            else:
                response = {
                    "inactive_message": "User is not active; please contact admin for assistance"
                }
        else:
            response = {
                "no_user_message": "User does not exist"
            }

        
        return json.dumps(response)

def get_all_users():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT 
            u.id,
            u.first_name,
            u.last_name,
            u.display_name,
            u.is_admin,
            u.active
        FROM users u
        """)

        dataset = db_cursor.fetchall()

        users = []

        for row in dataset:
            user = User(id = row["id"],
                        first_name = row["first_name"], 
                        last_name = row["last_name"], 
                        display_name = row["display_name"], 
                        user_name = None, 
                        password = None,
                        email = None, 
                        bio = None, 
                        created_on = None, 
                        is_admin = row["is_admin"],
                        active = row["active"])

            users.append(user.__dict__)

        return json.dumps(users)

def get_user_by_id(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.profile_image_url,
            u.display_name,
            u.email,
            u.created_on,
            u.is_admin,
            u.active
        FROM Users u
        WHERE id = ?
        """, (id,))

        data = db_cursor.fetchone()

        user = User(id = data["id"],
                    first_name = data["first_name"], 
                    last_name = data["last_name"], 
                    display_name = data["display_name"], 
                    user_name = None, 
                    password = None,
                    email = data["email"], 
                    bio = None, 
                    created_on = data["created_on"], 
                    is_admin = data["is_admin"],
                    profile_image_url = data["profile_image_url"],
                    active = data["active"])
        
        return json.dumps(user.__dict__)

def deactivate_user(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        UPDATE Users
        SET active = False
        WHERE id = ?
        """, (id,))

        rows_affected = db_cursor.rowcount

        success = False

        if rows_affected > 0:
            success = True
        
        return(success)

def activate_user(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        UPDATE Users
        SET active = True
        WHERE id = ?
        """, (id,))

        rows_affected = db_cursor.rowcount

        success = False

        if rows_affected > 0:
            success = True
        
        return(success)

def change_user_type(user_body):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        UPDATE Users
        SET is_admin = NOT is_admin
        WHERE id = ?
        """, (int(user_body["id"]),))

        rows_affected = db_cursor.rowcount

        if rows_affected > 0:
            return True
        else:
            return False