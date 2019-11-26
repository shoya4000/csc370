DROP TABLE IF EXISTS user_acc, Profile, Follows, Post, Content, PostTags, ProfileTags, Comment CASCADE;


CREATE TABLE user_acc (
	UserID  SERIAL PRIMARY KEY,
	Email VARCHAR(50),
	PermissionLevel BOOLEAN,
	Username VARCHAR(50) NOT NULL,
	Password VARCHAR(100) NOT NULL,
	CreationDate TIMESTAMP DEFAULT localtimestamp NOT NULL
);

CREATE TABLE Profile (
	ProfileID SERIAL PRIMARY KEY,
	Bio TEXT,
	ProfilePicture BYTEA,
	UserID INT REFERENCES user_acc(UserID)
);

CREATE TABLE Follows (
	FollowerProfileID INT REFERENCES Profile(ProfileID),
	FolloweeProfileID INT REFERENCES Profile(ProfileID),
	PRIMARY KEY(FollowerProfileID, FolloweeProfileID)
);

CREATE TABLE Post (
	PostID SERIAL PRIMARY KEY,
	CreationDate TIMESTAMP DEFAULT localtimestamp NOT NULL,
	Text TEXT,
	PermissionLevel BOOLEAN,
	ProfileID INT REFERENCES Profile(ProfileID),
	PostType VARCHAR(50)
);

CREATE TABLE Content (
	PostID INT,
	ContentID TEXT,
	PRIMARY KEY(PostID, ContentID)
);

CREATE TABLE PostTags (
	PostID INT,
	Tag TEXT,
	PRIMARY KEY(PostID, Tag)
);

CREATE TABLE ProfileTags (
	ProfileID INT,
	Tag TEXT,
PRIMARY KEY(ProfileID, Tag)
);

CREATE TABLE Comment (
	CommentID SERIAL PRIMARY KEY,
	CommentText TEXT NOT NULL,
	CreationDate TIMESTAMP DEFAULT localtimestamp NOT NULL,
	ProfileID INT REFERENCES Profile(ProfileID),
	PostID INT REFERENCES Post(PostID) ON DELETE cascade
);

INSERT INTO user_acc (Email, PermissionLevel, Username, Password) VALUES('mhauss@uvic.ca', TRUE, 'El Presidente', 'hotSTUFF1');
INSERT INTO user_acc (Email, PermissionLevel, Username, Password) VALUES('cdclarke@uvic.ca', TRUE, 'Chris', 'trevorsucks123');
INSERT INTO user_acc (Email, PermissionLevel, Username, Password) VALUES('martinroesli@uvic.ca', TRUE, 'Mroesli', 'abcdefg1234567');
INSERT INTO user_acc (Email, PermissionLevel, Username, Password) VALUES('thisistrevor@uvic.ca', TRUE, 'Trev', 'hiimtrevor123');
INSERT INTO user_acc (Email, PermissionLevel, Username, Password) VALUES('shoya@uvic.ca', TRUE, 'ShoYa', 'ShoYaPassword');
INSERT INTO user_acc (Email, PermissionLevel, Username, Password) VALUES('harperfriedman@uvic.ca', TRUE, 'NotPM', 'definitelyNot1234');

INSERT INTO Profile (Bio, ProfilePicture, UserID) VALUES ('Nunc nisl.', '\x52', 2);
INSERT INTO Profile (Bio, ProfilePicture, UserID) VALUES('Suspendisse potenti.', '\x01', 4);
INSERT INTO Profile (Bio, ProfilePicture, UserID) VALUES ('Vivamus tortor. convallis.', '\x5f', 6);
INSERT INTO Profile (Bio, ProfilePicture, UserID) VALUES ('Integer aliquet, lacinia sapien quis libero. Nullam sit amet turpis elementum ligula vehicula consequat.', '\xd4', 1);
INSERT INTO Profile (Bio, ProfilePicture, UserID) VALUES ('Corci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam.', '\xd9', 3);
INSERT INTO Profile (Bio, ProfilePicture, UserID) VALUES ('Donec justo. In hac habitasse platea dictumst.', '\x83', 6);

INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (1, 3);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (1, 6);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (1, 2);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (1, 5);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (2, 3);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (2, 1);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (3, 6);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (4, 3);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (4, 5);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (4, 6);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (4, 1);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (4, 2);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (5, 1);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (5, 2);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (5, 6);
INSERT INTO Follows (FollowerProfileID, FolloweeProfileId) VALUES (6, 5);


INSERT INTO Post (Text, PermissionLevel, ProfileID, PostType) VALUES ('this is sparta!', TRUE, 2, 'text');
INSERT INTO Post (Text, PermissionLevel, ProfileID, PostType) VALUES ('this is america!', TRUE, 1, 'text');
INSERT INTO Post (Text, PermissionLevel, ProfileID, PostType) VALUES ('this is outrageous!', TRUE, 3, 'text');
INSERT INTO Post (Text, PermissionLevel, ProfileID, PostType) VALUES ('this is madness!', TRUE, 4, 'text');
INSERT INTO Post (Text, PermissionLevel, ProfileID, PostType) VALUES ('this is just sad!', TRUE, 5, 'song');
INSERT INTO Post (Text, PermissionLevel, ProfileID, PostType) VALUES ('this is incredible!', TRUE, 6, 'playlist');


INSERT INTO ProfileTags (ProfileID, Tag) VALUES (1, 'Rock');
INSERT INTO ProfileTags (ProfileID, Tag) VALUES (2, 'pop');
INSERT INTO ProfileTags (ProfileID, Tag) VALUES (3, 'jazz');
INSERT INTO ProfileTags (ProfileID, Tag) VALUES (4, 'metal');
INSERT INTO ProfileTags (ProfileID, Tag) VALUES (5, 'hip hop');
INSERT INTO ProfileTags (ProfileID, Tag) VALUES (6, 'classical');


INSERT INTO PostTags (PostID, Tag) VALUES (1, 'pop');
INSERT INTO PostTags (PostID, Tag) VALUES (2, 'metal');
INSERT INTO PostTags (PostID, Tag) VALUES (3, 'jazz');
INSERT INTO PostTags (PostID, Tag) VALUES (4, 'folk');
INSERT INTO PostTags (PostID, Tag) VALUES (5, 'baroque');
INSERT INTO PostTags (PostID, Tag) VALUES (6, 'techno');

INSERT INTO Content (PostID, ContentID) VALUES (5, '/user/post/song/633444');
INSERT INTO Content (PostID, ContentID) VALUES (6, '/user/post/playlist/8655352');

INSERT INTO Comment (commentText, ProfileID, PostID) VALUES ('Very informative, thank you very much!', 1, 1);
INSERT INTO Comment (commentText, ProfileID, PostID) VALUES ('I know right?', 2, 1);
INSERT INTO Comment (commentText, ProfileID, PostID) VALUES ('Yell cheese if you read this', 3, 3);
INSERT INTO Comment (commentText, ProfileID, PostID) VALUES ('Where can I find more of this?', 4, 4);
INSERT INTO Comment (commentText, ProfileID, PostID) VALUES ('Brought tears to my eyes', 5, 5);
INSERT INTO Comment (commentText, ProfileID, PostID) VALUES ('Me too!!', 6, 5);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to shoya;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to shoya;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to mhauss;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to mhauss;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to martinroesli;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to martinroesli;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to harperfriedman;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to harperfriedman;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to cdclarke;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to cdclarke;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to trevorarutherford;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to trevorarutherford;