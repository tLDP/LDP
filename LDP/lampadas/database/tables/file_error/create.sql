CREATE TABLE file_error
(
	filename		TEXT		NOT NULL	REFERENCES sourcefile(filename),
	err_id			INT4		NOT NULL	REFERENCES error(err_id),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (filename, err_id)
);

CREATE INDEX file_error_upd_idx ON file_error (updated);
CREATE INDEX file_error_ctd_idx ON file_error (created);
