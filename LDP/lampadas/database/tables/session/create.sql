CREATE TABLE session (
	username	CHAR(20)	NOT NULL	UNIQUE	REFERENCES username(username),
	timestamp	TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (username)
);
