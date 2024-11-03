CREATE TABLE User(
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	display_name TEXT NOT NULL,
	role TEXT NOT NULL,
	banned BOOLEAN NOT NULL,
	unban_date DATETIME
);

CREATE TABLE Post(
	post_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	post_text TEXT,
	has_images BOOLEAN,
	repost_id INTEGER,
	date_and_time DATETIME NOT NULL,
	reply_id INTEGER,
);

CREATE TABLE Report(
	report_id INTEGER PRIMARY KEY AUTOINCREMENT,
	explaination TEXT NOT NULL,
	post_id INTEGER,
	reported_id INTEGER NOT NULL,
	reporter_id INTEGER NOT NULL,
	sorted BOOLEAN NOT NULL,
	date_and_time DATETIME NOT NULL
);

CREATE TABLE Notification(
	user_id INTEGER NOT NULL,
	interacting_user_id INTEGER NOT NULL,
	post_id INTEGER,
	action INTEGER NOT NULL,
	seen INTEGER NOT NULL,
	date_and_time DATETIME NOT NULL
);

CREATE TABLE Like(
	post_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL
);

CREATE TABLE Follow(
	follower_id INTEGER NOT NULL,
	followee_id INTEGER NOT NULL,
);
