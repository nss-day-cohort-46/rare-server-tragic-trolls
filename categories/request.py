
import sqlite3
import json
def create_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Categories
            (label)
        VALUES
            (?)
        """, (new_category['label'],))
        id = db_cursor.lastrowid
        new_category['id'] = id
    return json.dumps(new_category)