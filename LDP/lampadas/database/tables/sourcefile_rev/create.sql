CREATE TABLE sourcefile_rev
(
	rev_id			INT4		NOT NULL,
	filename		TEXT		NOT NULL	REFERENCES sourcefile(filename),
	version			CHAR(12)	NOT NULL,
	pub_date		DATE,
	initials		CHAR(3)		NOT NULL,
	notes			TEXT,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (rev_id)
);

CREATE INDEX sourcefile_rev_idx ON sourcefile_rev (filename);
