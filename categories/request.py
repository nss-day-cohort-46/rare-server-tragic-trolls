import sqlite3
import json
from models import Category

def get_all_categories():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        ORDER by label
        """)
        categories = []
        dataset = db_cursor.fetchall()
        for row in dataset :
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__)
    return json.dumps(categories)
def delete_category(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """,(id,))