DROP TABLE username;

CREATE TABLE username (
	user_id		INT4		NOT NULL,
	username	CHAR(20)	NOT NULL UNIQUE,
	session_id	CHAR(20),
	first_name	CHAR(20),
	surname		CHAR(20),
	email		TEXT,
	admin		BOOLEAN,
	password	CHAR(12),
	notes		TEXT,

	PRIMARY KEY (user_id)
);
