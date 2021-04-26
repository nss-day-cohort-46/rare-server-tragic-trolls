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
def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE from tags
        WHERE id = ?
        """,(id,))