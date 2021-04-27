import sqlite3
import json
from models import Post, Tag

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
        """)

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
            db_cursor.execute("""
            SELECT
                pt.id,
                pt.post_id,
                pt.tag_id,
                t.id,
                t.label
            FROM PostTags pt
            JOIN Tags t
                ON t.id = pt.tag_id
            WHERE pt.post_id = ?
            """, ( row['id'], ))
            post_tags = []
            tagdataset = db_cursor.fetchall()
            for tag_row in tagdataset:
                post_tag = Tag(tag_row['tag_id'], 
                            tag_row['label'])
                post_tags.append(post_tag.__dict__)
            post.tags = post_tags
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
            db_cursor.execute("""
            SELECT
                pt.id,
                pt.post_id,
                pt.tag_id,
                t.id,
                t.label
            FROM PostTags pt
            JOIN Tags t
                ON t.id = pt.tag_id
            WHERE pt.post_id = ?
            """, ( row['id'], ))
            post_tags = []
            tagdataset = db_cursor.fetchall()
            for tag_row in tagdataset:
                post_tag = Tag(tag_row['tag_id'], 
                            tag_row['label'])
                post_tags.append(post_tag.__dict__)
            post.tags = post_tags
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
        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id,
            t.id,
            t.label
        FROM PostTags pt
        JOIN Tags t
            ON t.id = pt.tag_id
        WHERE pt.post_id = ?
        """, ( single_post['id'], ))
        post_tags = []
        tagdataset = db_cursor.fetchall()
        for tag_row in tagdataset:
            post_tag = Tag(tag_row['tag_id'], 
                        tag_row['label'])
            post_tags.append(post_tag.__dict__)
        post.tags = post_tags
    return json.dumps(post.__dict__)

def create_post(new_post):
    new_post['approved'] = 0
    new_id = -1
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        Select is_admin
        FROM Users
        WHERE id = ?
        """, ( new_post['userId'], ))
        thePostCreator = db_cursor.fetchone()
        if thePostCreator[0] == 1:
            new_post['approved'] = 1
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
        new_id = db_cursor.lastrowid
        if new_post['tagIds']:
            for tag_id in new_post['tagIds']:
                db_cursor.execute("""
                INSERT INTO PostTags
                    ( post_id, tag_id )
                VALUES
                    ( ?, ? );
                """, (new_id, tag_id ))
    new_post_result = get_post_by_id(new_id)
    return new_post_result

def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))

        db_cursor.execute("""
        DELETE FROM PostTags
        WHERE post_id = ?
        """, (id, ))

def update_post(id, put_body):
    rows_affected = 0
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        if put_body['approved'] == True:
            db_cursor.execute("""
            Select is_admin
            FROM Users
            WHERE id = ?
            """, ( put_body['userId'], ))
            thePostCreator = db_cursor.fetchone()
            if thePostCreator[0] == 0:
                put_body['approved'] = False
        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """, ( put_body['userId'], 
                put_body['categoryId'],
                put_body['title'], 
                put_body['publicationDate'],
                put_body['imageUrl'], 
                put_body['content'], 
                put_body['approved'], 
                id ))
        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount
        if put_body['tagIds']:
            db_cursor.execute("""
            DELETE FROM PostTags
            WHERE post_id = ?
            """, (id, ))
            for tag_id in put_body['tagIds']:
                db_cursor.execute("""
                INSERT INTO PostTags
                    ( post_id, tag_id )
                VALUES
                    ( ?, ? );
                """, (id, tag_id ))
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def approve_post(approval_body):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Posts
            SET
                approved = 1
        WHERE id = ?
        """, ( approval_body['postId'], ))
        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True