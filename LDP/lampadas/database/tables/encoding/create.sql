CREATE TABLE encoding
(
	encoding		CHAR(12)	NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (encoding)
);

CREATE INDEX encoding_upd_idx ON encoding (updated);
CREATE INDEX encoding_ctd_idx ON encoding (created);
