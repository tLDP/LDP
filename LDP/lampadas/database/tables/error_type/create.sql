CREATE TABLE error_type
(
	err_type_code		CHAR(12)	NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (err_type_code)
);

CREATE INDEX error_type_upd_idx ON error_type (updated);
CREATE INDEX error_type_ctd_idx ON error_type (created);
