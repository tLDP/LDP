CREATE TABLE config (
	name			CHAR(20)	NOT NULL,
	value			TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (name)
);

CREATE INDEX config_upd_idx ON config (updated);
CREATE INDEX config_ctd_idx ON config (created);
