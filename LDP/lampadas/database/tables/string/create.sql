CREATE TABLE string
(
	string_code		CHAR(40)	NOT NULL,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (string_code)
);


