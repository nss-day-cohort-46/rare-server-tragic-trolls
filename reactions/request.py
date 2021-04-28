from models.post_reaction import Post_Reaction
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

def get_reactions_by_post_id(post_id):
  with sqlite3.connect('./rare.db') as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT 
      pr.id,
      pr.user_id,
      pr.reaction_id,
      pr.post_id,
      r.label,
      r.image_url,
      COUNT(reaction_id)
    FROM PostReactions pr
    JOIN Reactions r on r.id = pr.reaction_id
    WHERE post_id = ?
    GROUP BY pr.reaction_id
    """, [post_id, ])

    post_reactions = []

    dataset = db_cursor.fetchall()

    for data in dataset:
      post_reaction = Post_Reaction(data['id'], data['user_id'], data['reaction_id'], data['post_id'])
      #TODO: make a "Reaction" model and get the data from the rows for it.
      #Then append the reaction to post_reaction.
      post_reaction.count = data['COUNT']
    
      post_reactions.append(post_reaction.__dict__)

