CREATE TABLE username (
	username	CHAR(40)	NOT NULL UNIQUE,
	session_id	CHAR(20),
	first_name	CHAR(25),
	middle_name	CHAR(25),
	surname		CHAR(25),
	email		TEXT,
	admin		BOOLEAN		DEFAULT False,
	sysadmin	BOOLEAN		DEFAULT False,
	password	CHAR(12),
	notes		TEXT,
	stylesheet	CHAR(12)	DEFAULT 'default',

	PRIMARY KEY (username)
);
