CREATE TABLE sourcefile_metadata
(
	filename		TEXT		NOT NULL	REFERENCES sourcefile(filename),
	dtd_code		CHAR(12)			REFERENCES dtd(dtd_code),
	dtd_version		CHAR(12),
	title			TEXT,
	abstract		TEXT,
	version			CHAR(12),
	pub_date		TEXT,
	isbn			TEXT,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP,	
	
	PRIMARY KEY (filename)
);
