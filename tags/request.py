import sqlite3
import json
from models import Tag

def get_all_tags():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        ORDER by label
        """)
        tags = []
        dataset = db_cursor.fetchall()
        for row in dataset :
            tag = Tag(row['id'], row['label'])
            tags.append(tag.__dict__)
    return json.dumps(tags)
def update_tag(id, updated_tag):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE tags
            SET 
                label = ?
        WHERE id = ?
        """,(updated_tag['label'], id))
        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            return False
        else:
            return True
def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE from tags
        WHERE id = ?
        """,(id,))
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