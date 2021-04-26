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

def get_post_by_id(id):

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
        WHERE p.id = ?
        """, (id, ))

        single_post = db_cursor.fetchone()

        post = Post(single_post['id'], 
                    single_post['user_id'], 
                    single_post['category_id'],
                    single_post['title'], 
                    single_post['publication_date'],
                    single_post['image_url'], 
                    single_post['content'], 
                    single_post['approved'])

    return json.dumps(post.__dict__)