CREATE TABLE session (
	username	CHAR(20)	NOT NULL	UNIQUE	REFERENCES username(username),
	timestamp	TIMESTAMP	NOT NULL	DEFAULT now(),
	ip_address	CHAR(15),

	PRIMARY KEY (username)
);
