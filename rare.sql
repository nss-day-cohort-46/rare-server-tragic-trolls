CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit,
  "is_admin" bit
);

INSERT INTO Users
  ('first_name', 'last_name', 'email', 'bio', 'username', 'password', 'created_on', 'active', 'is_admin')
VALUES  
  ('test', 'user', 'test@user.com', 'bio', 'test@user.com', 'password', '12/31/2020', True, True);
INSERT INTO Users
  ('first_name', 'last_name', 'email', 'bio', 'username', 'password', 'created_on', 'active', 'is_admin')
VALUES  
  ('test', 'user', 'test@user.com', 'bio', 'test@user.com', 'password', '12/31/2020', True, False);

DELETE FROM Users
WHERE id = 1;

SELECT * FROM users;

SELECT
    *
FROM users
WHERE username = 'test@user.com' and password = 'password';

DROP Table Users;

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

ALTER TABLE Subscriptions ADD COLUMN "ended_on" DATE;

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 1, 2, 'Title#1', '2021-04-02T23:57:07.374Z', '', 'Post Text #1', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 2, 3, 'Title#2', '2022-04-02T23:57:07.374Z', '', 'Post Text #2', 0);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 1, 4, 'Title#3', '2023-04-02T23:57:07.374Z', '', 'Post Text #3', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 2, 2, 'Title#4', '2024-04-02T23:57:07.374Z', '', 'Post Text #4', 0);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 1, 3, 'Title#5', '2025-04-02T23:57:07.374Z', '', 'Post Text #5', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 2, 4, 'Title#6', '2026-04-02T23:57:07.374Z', '', 'Post Text #6', 0);


DROP TABLE Posts

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
WHERE p.user_id = 1

SELECT
    pt.id,
    pt.post_id,
    pt.tag_id
FROM PostTags pt
WHERE pt.post_id = 2

SELECT
    pt.id,
    pt.post_id,
    pt.tag_id,
    t.id,
    t.label
FROM PostTags pt
JOIN Tags t
    ON t.id = pt.tag_id
WHERE pt.post_id = 1

Select is_admin
FROM Users
WHERE id = 2

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
WHERE s.follower_id = 6
AND s.ended_on = "" OR s.ended_on IS NULL

INSERT INTO Subscriptions (id, follower_id, author_id, created_on, ended_on)
VALUES ( 50, 5, 6, '2021-04-02T23:57:07.374Z', '' );
INSERT INTO Subscriptions (id, follower_id, author_id, created_on, ended_on)
VALUES ( 51, 6, 5, '2021-04-02T23:57:07.374Z', '' );

INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') 
VALUES (50, 5, 1, 'Title#1', '2021-04-02T23:57:07.374Z', '', 'Post Text #1', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') 
VALUES (51, 5, 1, 'Title#2', '2022-04-02T23:57:07.374Z', '', 'Post Text #2', 0);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') 
VALUES (52, 5, 1, 'Title#3', '2023-04-02T23:57:07.374Z', '', 'Post Text #3', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') 
VALUES (53, 6, 1, 'Title#4', '2024-04-02T23:57:07.374Z', '', 'Post Text #4', 0);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') 
VALUES (54, 6, 1, 'Title#5', '2025-04-02T23:57:07.374Z', '', 'Post Text #5', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') 
VALUES (55, 6, 1, 'Title#6', '2026-04-02T23:57:07.374Z', '', 'Post Text #6', 0);

INSERT INTO Users
  ('id', 'first_name', 'last_name', 'email', 'bio', 'username', 'password', 'created_on', 'active', 'is_admin')
VALUES  
  (5, 'fifth', 'user', 'test@user.com', 'bio', 'test@user.com', 'password', '12/31/2020', True, True);
INSERT INTO Users
  ('id', 'first_name', 'last_name', 'email', 'bio', 'username', 'password', 'created_on', 'active', 'is_admin')
VALUES  
  (6, 'sixth', 'user', 'test@user.com', 'bio', 'test@user.com', 'password', '12/31/2020', True, False);


SELECT
    p.id,
    p.user_id,
    p.category_id,
    p.title,
    p.publication_date,
    p.image_url,
    p.content,
    p.approved,
    c.id as the_category_id,
    c.label,
    u.id as the_user_id,
    u.first_name,
    u.last_name,
    u.display_name,
    u.is_admin,
    u.active
FROM posts p
left JOIN categories c 
    ON p.category_id = the_category_id
left JOIN users u
    ON p.user_id = the_user_id
WHERE title LIKE "%first%"
