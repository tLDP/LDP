CREATE TABLE role(
	role_code		CHAR(12)	NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (role_code)
);

CREATE INDEX role_upd_idx ON role (updated);
CREATE INDEX role_ctd_idx ON role (created);
