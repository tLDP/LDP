DROP TABLE license;

CREATE TABLE license
(
	license			CHAR(12)	NOT NULL,

	PRIMARY KEY (license)
);

GRANT SELECT ON license TO "www-data";

