CREATE TABLE file_error
(
	filename		TEXT		NOT NULL	REFERENCES document_file(filename),
	err_id			INT4		NOT NULL	REFERENCES error(err_id),
	date_entered		TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (filename, err_id)
);
