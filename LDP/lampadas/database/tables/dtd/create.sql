CREATE TABLE dtd
(
	dtd_code		CHAR(12)	NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (dtd_code)
);

CREATE INDEX dtd_upd_idx ON dtd (updated);
CREATE INDEX dtd_ctd_idx ON dtd (created);
