DROP TABLE dtd;

CREATE TABLE dtd
(
	dtd			CHAR(12)	NOT NULL,

	PRIMARY KEY (dtd)
);

GRANT SELECT ON dtd TO "www-data";

