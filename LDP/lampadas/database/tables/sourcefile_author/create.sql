CREATE TABLE sourcefile_author
(
	filename		TEXT		NOT NULL	REFERENCES sourcefile(filename),
	firstname		TEXT,
	othername		TEXT,
	surname			TEXT,
	email			TEXT,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now()
);

CREATE INDEX sourcefile_author_idx ON sourcefile_author (filename);

CREATE INDEX sourcefile_author_upd_idx ON sourcefile_author (updated);
CREATE INDEX sourcefile_author_ctd_idx ON sourcefile_author (created);
