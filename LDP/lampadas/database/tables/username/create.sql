CREATE TABLE username (
	username		CHAR(40)	NOT NULL UNIQUE,
	session_id		CHAR(20),
	first_name		CHAR(25),
	middle_name		CHAR(25),
	surname			CHAR(25),
	email			TEXT,
	admin			BOOLEAN		DEFAULT False,
	sysadmin		BOOLEAN		DEFAULT False,
	password		CHAR(12),
	notes			TEXT,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (username)
);

CREATE INDEX username_upd_idx ON username (updated);
CREATE INDEX username_ctd_idx ON username (created);
