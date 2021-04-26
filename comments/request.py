from models import Comment
import sqlite3
import json

def get_all_comments():
  with sqlite3.connect('./rare.db') as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT
      c.id,
      c.post_id,
      c.author_id,
      c.content,
      c.subject,
      c.created_on
    FROM comments c
    """)

    comments = []

    dataset = db_cursor.fetchall()

    for data in dataset:
      comment = Comment(data['id'], data['post_id'], data['author_id'], data['content'], data['subject'], data['created_on'])

      comments.append(comment.__dict__)
    
  return json.dumps(comments)

def create_comment(post_id, new_comment):
  with sqlite3.connect('./rare.db') as conn:
    db_cursor = conn.cursor()

    db_cursor.execute("""
    INSERT INTO comments
      (post_id, author_id, content, subject, created_on)
    VALUES
      (?, ?, ?, ?, ?)
    """, (post_id, new_comment['author_id'], 
          new_comment['content'], new_comment['subject'], 
          new_comment['created_on']))

    id = db_cursor.lastrowid

    new_comment['id'] = id

  return json.dumps(new_comment)