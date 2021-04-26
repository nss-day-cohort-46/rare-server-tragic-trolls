import sqlite3
import json
from models import Post

def get_posts_by_user_id(user_id):

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            CASE [approved]
            WHEN 1 then  'True'
            WHEN 0 then 'False'
            ELSE 'NA'
            END AS [approved]
        FROM posts p
        WHERE p.user_id = ?
        """, (user_id, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], 
                        row['user_id'], 
                        row['category_id'],
                        row['title'], 
                        row['publication_date'],
                        row['image_url'], 
                        row['content'], 
                        row['approved'])
            posts.append(post.__dict__)

    return json.dumps(posts)