CREATE TABLE sourcefile
(
	filename		TEXT		NOT NULL,
	format_code		CHAR(20)	REFERENCES format(format_code),
	dtd_code		CHAR(12)	REFERENCES dtd(dtd_code),
	dtd_version		CHAR(12),
	filesize		INT4,
	filemode		CHAR(20),
	modified		TIMESTAMP,
	full_text		TEXT,

	PRIMARY KEY (filename)
);
