CREATE TABLE username (
	username	CHAR(20)	NOT NULL UNIQUE,
	session_id	CHAR(20),
	first_name	CHAR(20),
	middle_name	CHAR(20),
	surname		CHAR(20),
	email		TEXT,
	admin		BOOLEAN		DEFAULT False,
	sysadmin	BOOLEAN		DEFAULT False,
	password	CHAR(12),
	notes		TEXT,
	stylesheet	CHAR(12),

	PRIMARY KEY (username)
);
