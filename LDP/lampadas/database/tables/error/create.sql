CREATE TABLE error
(
	err_id			INT4		NOT NULL,
	err_type_code		CHAR(12)	NOT NULL REFERENCES error_type(err_type_code),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (err_id)
);
