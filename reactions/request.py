import sqlite3
import json 

def add_reaction(post_id, new_reaction):
  with sqlite3.connect('./rare.db') as conn:
    db_cursor = conn.cursor()

    db_cursor.execute("""
    INSERT INTO PostReactions
      (user_id, reaction_id, post_id)
    VALUES
      (?, ?, ?)
    """, (new_reaction['user_id'], new_reaction['reaction_id'], post_id))

    id = db_cursor.lastrowid

    new_reaction['id'] = id
  return json.dumps(new_reaction)