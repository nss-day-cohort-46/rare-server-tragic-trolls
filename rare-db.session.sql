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

DROP TABLE Users;

INSERT INTO Users
VALUES 
( NULL, "test", "user", "test@user.com", "test", "test@user.com",
  "bio", "password", "", "2020-01-03", TRUE, FALSE
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

DROP TABLE PostReactions;

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
INSERT INTO Reactions ('label', 'image_url') VALUES ('what', 'https://pngtree.com/so/happy');
INSERT INTO Users ('first_name', 'last_name', 'email', 'bio', 'username', 'password', 'profile_image_url', 'created_on', 'active') VALUES ('phil', 'phan', 'a@b.c', 'it me', 'philphan', 'password', 'https://pngtree.com/so/happy', '2020-01-01', 1);
INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content', 'approved') VALUES (1, 1, 'new post', '2021-01-01', 'https://pngtree.com/so/happy', 'testing post', 1)
INSERT INTO comments ('post_id', 'author_id', 'content', 'subject', 'created_on') VALUES (1, 1, 'test', 'test', '2021-01-01')


SELECT * FROM Comments

DELETE FROM Comments

DROP TABLE Comments

DROP TABLE PostReactions

INSERT INTO Reactions ('label', 'image_url')
VALUES ('YeeHaw', 'https://res.cloudinary.com/nicecloudbro/image/upload/v1619711464/yeehaw_gft31j.png');
INSERT INTO Reactions ('label', 'image_url')
VALUES ('YeeNah', 'https://res.cloudinary.com/nicecloudbro/image/upload/v1619711737/yeenah_cs7dwm.png');
INSERT INTO Reactions ('label', 'image_url')
VALUES ('TwoFingersTouch', 'https://res.cloudinary.com/nicecloudbro/image/upload/v1619711762/twofingerstouch_tu86cq.png');
INSERT INTO PostReactions ('user_id', 'reaction_id', 'post_id')
VALUES (1, 1, 1);
INSERT INTO PostReactions ('user_id', 'reaction_id', 'post_id')
VALUES (1, 1, 1);
INSERT INTO PostReactions ('user_id', 'reaction_id', 'post_id')
VALUES (1, 2, 1)


INSERT INTO comments ('post_id', 'author_id', 'content', 'subject', 'created_on') VALUES (1, 1, 'test', 'test', '2021-01-01');


SELECT * FROM Users;

UPDATE Users
        SET is_admin = NOT is_admin
        WHERE id = 1;

INSERT INTO users
            ('first_name', 'last_name', 'display_name', 'email', 'bio', 'username', 'password', 'created_on', 'profile_image_url', 'is_admin', 'active')
        VALUES
            ('first_name', 'last_name', 'display_name', 'email', 'bio', 'username', 'password', 'Wednesday, April 28, 2021', 'https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png', FALSE, FALSE);


        SELECT 
            pr.id,
            pr.user_id,
            pr.reaction_id,
            pr.post_id,
            r.label,
            r.image_url
        FROM PostReactions pr
        JOIN Reactions r ON r.id = pr.reaction_id
        WHERE pr.post_id = 1