DROP TABLE username;

CREATE TABLE username (
	user_id		INT4		NOT NULL,
	username	CHAR(20)	NOT NULL UNIQUE,
	session_id	CHAR(20),
	first_name	CHAR(20),
	middle_name	CHAR(20),
	surname		CHAR(20),
	email		TEXT,
	admin		BOOLEAN,
	sysadmin	BOOLEAN,
	password	CHAR(12),
	notes		TEXT,
	stylesheet	CHAR(12),

	PRIMARY KEY (user_id)
);
