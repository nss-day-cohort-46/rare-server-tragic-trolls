from models.postreaction import Post_Reaction
from models.reaction import Reaction
import sqlite3
import json 

def add_reaction(new_reaction):
  with sqlite3.connect('./rare.db') as conn:
    db_cursor = conn.cursor()

    db_cursor.execute("""
    INSERT INTO PostReactions
      (user_id, reaction_id, post_id)
    VALUES
      (?, ?, ?)
    """, (new_reaction['user_id'], new_reaction['reaction_id'], new_reaction['post_id']))

    id = db_cursor.lastrowid

    new_reaction['id'] = id
  return json.dumps(new_reaction)

def create_reaction(new_reaction):
  with sqlite3.connect('./rare.db') as conn:
    db_cursor = conn.cursor()

    db_cursor.execute("""
    INSERT INTO Reactions
      (label, image_url)
    VALUES
      (?, ?)
    """, (new_reaction['label'], new_reaction['image_url']))

    id = db_cursor.lastrowid

    new_reaction['id'] = id

  return json.dumps(new_reaction)

def get_all_reactions():
  with sqlite3.connect('./rare.db') as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT
      r.id,
      r.label,
      r.image_url
    FROM Reactions r
    """)

    reactions = []

    dataset = db_cursor.fetchall()

    for data in dataset:
      reaction = Reaction(data['id'], data['label'], data['image_url'])
      reactions.append(reaction.__dict__)

  return json.dumps(reactions)

def get_postreactions_by_id(post_id):
  with sqlite3.connect('./rare.db') as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT
      pr.id,
      pr.user_id,
      pr.reaction_id,
      pr.post_id
    FROM PostReactions pr
    WHERE pr.post_id = ?
    """, (post_id, ))

    postreactions = []

    dataset = db_cursor.fetchall()

    for data in dataset:
      postreaction = Post_Reaction(data['id'], data['user_id'], data['reaction_id'], data['post_id'])
      postreactions.append(postreaction.__dict__)

  return json.dumps(postreactions)
