CREATE TABLE session (
	username	CHAR(40)	NOT NULL	UNIQUE	REFERENCES username(username),
	timestamp	TIMESTAMP	NOT NULL	DEFAULT now(),
	ip_address	CHAR(15),
	uri		TEXT,

	PRIMARY KEY (username)
);
