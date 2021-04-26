import sqlite3
import json
def create_tag(new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Tags
            (label)
        VALUES
            (?)
        """, (new_tag['label'],))
        id = db_cursor.lastrowid
        new_tag['id'] = id
    return json.dumps(new_tag) 