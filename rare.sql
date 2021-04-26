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
  "active" bit
);

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

INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 1, 1, 'Title#1', '2021-04-02T23:57:07.374Z', 'https://res.cloudinary.com/nch66862/image/upload/v1617690859/man19_mfb18l.jpg', 'Post Text #1', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 2, 1, 'Title#2', '2022-04-02T23:57:07.374Z', 'https://res.cloudinary.com/nch66862/image/upload/v1617690859/man19_mfb18l.jpg', 'Post Text #2', 0);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 1, 1, 'Title#3', '2023-04-02T23:57:07.374Z', 'https://res.cloudinary.com/nch66862/image/upload/v1617690859/man19_mfb18l.jpg', 'Post Text #3', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 2, 1, 'Title#4', '2024-04-02T23:57:07.374Z', 'https://res.cloudinary.com/nch66862/image/upload/v1617690859/man19_mfb18l.jpg', 'Post Text #4', 0);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 1, 1, 'Title#5', '2025-04-02T23:57:07.374Z', 'https://res.cloudinary.com/nch66862/image/upload/v1617690859/man19_mfb18l.jpg', 'Post Text #5', 1);
INSERT INTO Posts ('id', 'user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (Null, 2, 1, 'Title#6', '2026-04-02T23:57:07.374Z', 'https://res.cloudinary.com/nch66862/image/upload/v1617690859/man19_mfb18l.jpg', 'Post Text #6', 0);


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