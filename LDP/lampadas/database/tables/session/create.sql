CREATE TABLE session (
	username	CHAR(20)	NOT NULL	UNIQUE	REFERENCES username(username),
	timestamp	DATE				DEFAULT now(),

	PRIMARY KEY (username)
);
