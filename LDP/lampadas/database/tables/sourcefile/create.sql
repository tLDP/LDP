CREATE TABLE sourcefile
(
	filename		TEXT		NOT NULL,
	filesize		INT4,
	filemode		CHAR(20),
	format_code		CHAR(20)			REFERENCES format(format_code),
	dtd_code		CHAR(12)			REFERENCES dtd(dtd_code),
	dtd_version		CHAR(12),
	title			TEXT,
	abstract		TEXT,
	version			CHAR(12),
	pub_date		TEXT,
	isbn			TEXT,
	encoding		CHAR(12),
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),
	
	PRIMARY KEY (filename)
);
