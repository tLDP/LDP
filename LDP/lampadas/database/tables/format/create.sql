CREATE TABLE format
(
	format_code		CHAR(20)	NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (format_code)
);

CREATE INDEX format_upd_idx ON format (updated);
CREATE INDEX format_ctd_idx ON format (created);
