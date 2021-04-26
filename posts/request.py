import sqlite3
import json
from models import Post

def get_all_posts():

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
            p.approved
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
            if post.approved == 0:
                post.approved = False
            else:
                post.approved = True
            posts.append(post.__dict__)

    return json.dumps(posts)

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
            p.approved
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
            if post.approved == 0:
                post.approved = False
            else:
                post.approved = True
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
            p.approved
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

        if post.approved == 0:
            post.approved = False
        else:
            post.approved = True

    return json.dumps(post.__dict__)

def create_post(new_post):
    new_post['approved'] = 1
    if 'imageUrl' not in new_post:
        new_post['imageUrl'] = ""
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id,
                category_id,
                title,
                publication_date,
                image_url,
                content,
                approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ? );
        """, (new_post['userId'], 
                new_post['categoryId'],
                new_post['title'],
                new_post['publicationDate'], 
                new_post['imageUrl'],
                new_post['content'],
                new_post['approved'], )
        )

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['approved'] = True
        new_post['id'] = id


    return new_post