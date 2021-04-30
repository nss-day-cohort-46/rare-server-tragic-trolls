DROP TABLE Users;
DROP TABLE Categories;
DROP TABLE Comments;
DROP TABLE DemotionQueue;
DROP TABLE PostReactions;
DROP TABLE PostTags;
DROP TABLE Posts;
DROP TABLE Reactions;
DROP TABLE Subscriptions;
DROP TABLE Tags;

CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "username" varchar,
  "display_name" varchar,
  "email" varchar,
  "bio" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit,
  "is_admin" bit
);

INSERT INTO Users
(id, first_name, last_name, username, display_name, email, bio, password, profile_image_url, created_on, active, is_admin)
VALUES (NULL, "Kaitlin", "Kelley", "kaitlin@kaitlin.com", "Kaitlin", "kaitlin@kaitlin.com", "I am admin", "password", "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png", "Friday, April 30, 2021", True, True),
  (NULL, "Jake", "Froeb", "jake@jake.com", "Jake", "jake@jake.com", "I am admin", "password", "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png", "Friday, April 30, 2021", True, True),
  (NULL, "Phillip", "Phan", "phillip@phillip.com", "Phillip", "phillip@phillip.com", "I am admin", "password", "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png", "Friday, April 30, 2021", True, True),
  (NULL, "Nick", "Carver", "nick@nick.com", "Nick", "nick@nick.com", "I am admin", "password", "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png", "Friday, April 30, 2021", True, True),
  (NULL, "Admin", "User", "admin@admin.com", "Admin", "admin@admin.com", "I am admin", "password", "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png", "Friday, April 30, 2021", True, True);

CREATE TABLE "DemotionQueue" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  "ended_on" date,
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
  "approved" bit,
  FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY (`category_id`) REFERENCES `Categories`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  "subject" varchar,
  "created_on" date,
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

CREATE TABLE "Categories" (
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

