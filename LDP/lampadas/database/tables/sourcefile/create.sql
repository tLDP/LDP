CREATE TABLE sourcefile
(
	filename		TEXT		NOT NULL,
	format_code		CHAR(20)			REFERENCES format(format_code),
	filesize		INT4,
	filemode		CHAR(20),
	modified		TIMESTAMP,

	PRIMARY KEY (filename)
);
