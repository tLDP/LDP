CREATE TABLE username_notes
(
	username		CHAR(20)	NOT NULL	REFERENCES username(username),
	date_entered		TIMESTAMP	NOT NULL DEFAULT now(),
	notes			TEXT,
	creator			CHAR(20)	NOT NULL	REFERENCES username(username),

	PRIMARY KEY (username, date_entered)
);
