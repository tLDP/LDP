CREATE TABLE session (
	username		CHAR(40)	NOT NULL	UNIQUE	REFERENCES username(username),
	ip_address		CHAR(15),
	uri			TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (username)
);
