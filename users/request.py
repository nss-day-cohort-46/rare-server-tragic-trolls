import sqlite3
import json
from models import User, user

def register_new_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor() 

        new_user_object = User(id = None,
                                first_name = new_user["first_name"],
                                last_name = new_user["last_name"],
                                display_name = new_user["display_name"],
                                username = new_user["username"], 
                                email = new_user["email"],
                                password = new_user["password"],
                                bio = new_user["bio"],
                                created_on = new_user["created_on"],
                                profile_image_url = new_user["profile_image_url"])

        new_user_object = new_user_object.__dict__

        db_cursor.execute(""" 
        INSERT INTO users
            ('first_name', 'last_name', 'display_name', 'email', 'bio', 'username', 'password', 'created_on', 'profile_image_url', 'is_admin', 'active')
        VALUES
            (?,?,?,?,?,?,?,?,?,?,?)
        """, (new_user_object["firstName"], 
                new_user_object["lastName"],
                new_user_object["displayName"], 
                new_user_object["email"], 
                new_user_object["bio"], 
                new_user_object["username"], 
                new_user_object["password"], 
                new_user_object["createdOn"],
                new_user_object["profileImageUrl"],
                new_user_object["isAdmin"],
                new_user_object["active"]
        ))

        id = db_cursor.lastrowid

        response = {
            "valid": "valid",
            "token": id
        }

        return json.dumps(response)

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
                        username = None, 
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
                    username = None, 
                    password = None,
                    email = data["email"], 
                    bio = None, 
                    created_on = data["created_on"], 
                    is_admin = data["is_admin"],
                    profile_image_url = data["profile_image_url"],
                    active = data["active"])

        user = user.__dict__
                    
        db_cursor.execute(""" 
        SELECT
            s.id
        FROM Subscriptions s
        WHERE author_id = ? and ended_on = ""
        """, (id,))

        subscription_dataset = db_cursor.fetchall()

        subscriber_count = []

        for subscription_id in subscription_dataset:
            subscriber_count.append(subscription_id)
        user["subscribers"] = len(subscriber_count)
        
        return json.dumps(user)

def change_active_status(user_body):

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        rows_affected = None

        user_to_change = json.loads(get_user_by_id(int(user_body["user_id"])))

        if user_body["user_id"] != user_body["approver_one_id"]:
            if user_to_change["active"] == True:
                db_cursor.execute(""" 
                SELECT approver_one_id, action
                FROM DemotionQueue
                WHERE admin_id = ?
                """, (user_to_change["id"],))

                dataset = db_cursor.fetchall()
                action_row = None

                for row in dataset:
                    if row["action"] == "deactivate":
                        action_row = row

                if action_row is not None:
                    if int(user_body["approver_one_id"]) != action_row["approver_one_id"]:
                        db_cursor.execute(""" 
                        UPDATE Users
                        SET active = NOT active
                        WHERE id = ?
                        """, (int(user_body["user_id"]),))

                        db_cursor.execute(""" 
                        DELETE FROM DemotionQueue
                        WHERE admin_id = ? and action = "deactivate"
                        """, (user_to_change["id"],))

                        return True
                    else:
                        return "Deactivating an admin user requires approval from 2 separate admin users"
                else:
                    db_cursor.execute(""" 
                    INSERT INTO DemotionQueue
                    (action, admin_id, approver_one_id)
                    VALUES (?,?,?)
                    """, (user_body["action"], int(user_body["user_id"]), int(user_body["approver_one_id"])))

                    return True
            else:
                db_cursor.execute(""" 
                UPDATE Users
                SET active = NOT active
                WHERE id = ?
                """, (int(user_body["user_id"]),))

                rows_affected = db_cursor.rowcount
        else:
            return "Error: Admin cannot approve their own status change"

        if rows_affected > 0:
            return True
        else:
            return False
        
def change_user_type(user_body):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        rows_affected = None

        user_to_change = json.loads(get_user_by_id(int(user_body["user_id"])))

        if user_body["user_id"] != user_body["approver_one_id"]:
            if user_to_change["isAdmin"] == True:
                db_cursor.execute(""" 
                SELECT approver_one_id, action
                FROM DemotionQueue
                WHERE admin_id = ?
                """, (user_to_change["id"],))

                dataset = db_cursor.fetchall()
                action_row = None

                for row in dataset:
                    if row["action"] == "demote":
                        action_row = row

                if action_row is not None:
                    if int(user_body["approver_one_id"]) != action_row["approver_one_id"]:
                        db_cursor.execute(""" 
                        UPDATE Users
                        SET is_admin = NOT is_admin
                        WHERE id = ?
                        """, (int(user_body["user_id"]),))

                        db_cursor.execute(""" 
                        DELETE FROM DemotionQueue
                        WHERE admin_id = ? and action = "demote"
                        """, (user_to_change["id"],))

                        return True
                    else:
                        return "Demoting an admin user requires approval from 2 separate admin users"
                else:
                    # create new demotionqueue
                    db_cursor.execute(""" 
                    INSERT INTO DemotionQueue
                        (action, admin_id, approver_one_id)
                    VALUES (?,?,?)
                    """, (user_body["action"], int(user_body["user_id"]), int(user_body["approver_one_id"])))

                    return True
            else:
                db_cursor.execute(""" 
                UPDATE Users
                SET is_admin = NOT is_admin
                WHERE id = ?
                """, (int(user_body["user_id"]),))

                rows_affected = db_cursor.rowcount
        else:
            return "Error: Admin cannot approve their own status change"

        if rows_affected > 0:
            return True
        else:
            return False

def get_users_by_profile_type(query):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        boolean_query = None

        users = []

        if query.title() == "False":
            boolean_query = 0
        elif query.title() == "True":
            boolean_query = 1
        else: 
            users = "Error: Query was not a boolean"

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
            u.active,
            u.username,
            u.bio
        FROM users u
        WHERE is_admin = ?
        """, (boolean_query,))

        dataset = db_cursor.fetchall()

        for row in dataset:
            user = User(id = row["id"],
                    first_name = row["first_name"], 
                    last_name = row["last_name"], 
                    display_name = row["display_name"], 
                    username = row["username"], 
                    password = None,
                    email = row["email"], 
                    bio = row["bio"], 
                    created_on = row["created_on"], 
                    is_admin = row["is_admin"],
                    profile_image_url = row["profile_image_url"],
                    active = row["active"])
            
            users.append(user.__dict__)
        
        return json.dumps(users)