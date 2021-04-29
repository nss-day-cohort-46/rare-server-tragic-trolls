from models.reaction import Reaction
import sqlite3
import json
from models import Post, Tag, Comment

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

        db_cursor.execute("""
        SELECT 
            pr.id,
            pr.user_id,
            pr.reaction_id,
            pr.post_id,
            r.label,
            r.image_url,
            COUNT(reaction_id) count
        FROM PostReactions pr
        JOIN Reactions r ON r.id = pr.reaction_id
        WHERE pr.post_id = ?
        GROUP BY reaction_id
        """, (single_post['id'], ))
        post_reactions = []
        dataset = db_cursor.fetchall()
        for data in dataset:
            post_reaction = Reaction(data['reaction_id'], data['label'], data['image_url'])
            post_reaction.count = data['count']
            post_reactions.append(post_reaction.__dict__)
        post.reactions = post_reactions

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content,
            c.subject,
            c.created_on
        FROM Comments c
        WHERE c.post_id = ?
        ORDER BY c.id DESC
        """, (id, ))
        comments = []
        dataset = db_cursor.fetchall()
        for data in dataset:
            comment = Comment(data['id'], data['post_id'], data['author_id'],
                        data['content'], data['subject'], data['created_on'])
            comments.append(comment.__dict__)
        post.comments = comments
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

def approve_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Posts
            SET
                approved = 1
        WHERE id = ?
        """, ( id, ))
        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True

def subscribing_to_post(post_body):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( follower_id,
                author_id,
                created_on,
                ended_on )
        VALUES
            ( ?, ?, ?, ? );
        """, (post_body['follower_id'], 
                post_body['author_id'],
                post_body['created_on'],
                post_body['ended_on'] )
        )
        new_id = db_cursor.lastrowid
        post_body['id'] = new_id
        return json.dumps(post_body)

def get_subscribed_posts_by_id(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            s.id as subscription_id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on
        FROM posts p
        JOIN subscriptions s
            ON s.author_id = p.user_id
        WHERE s.follower_id = ?
        AND s.ended_on = "" OR s.ended_on IS NULL
        """, (id, ))

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

def unsubscribing_to_post(patch_body):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on,
            s.ended_on
        FROM subscriptions s
        WHERE s.follower_id = ?
        AND s.author_id = ?
        AND (s.ended_on = "" OR s.ended_on IS NULL)
        """, (patch_body['follower_id'],
                patch_body['author_id'], ))
        
        data = db_cursor.fetchone()
        id_to_update = data['id']

        db_cursor.execute("""
        UPDATE Subscriptions
        SET
            ended_on = ?
        WHERE id = ?
        """, ( patch_body['ended_on'],
            id_to_update ))

        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True

def get_posts_by_category_id(category_id):

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
        WHERE p.category_id = ?
        """, (category_id, ))

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

def get_posts_by_tag_id(tag_id):

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
            p.approved,
            pt.id as post_tag_id,
            pt.post_id,
            pt.tag_id
        FROM posts p
        JOIN PostTags pt
            ON p.id = pt.post_id
        WHERE tag_id = ?
        """, (tag_id, ))

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