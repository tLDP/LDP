DROP TABLE config;

CREATE TABLE config (
	name		CHAR(20)	NOT NULL,
	value		TEXT,

	PRIMARY KEY (name)
);

GRANT ALL ON config TO "www-data";
GRANT ALL on config to root;
