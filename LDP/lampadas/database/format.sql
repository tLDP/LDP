DROP TABLE format;

CREATE TABLE format
(
	format			CHAR(12)	NOT NULL,
	format_name		TEXT		NOT NULL,

	PRIMARY KEY (format)
);

GRANT SELECT ON format TO "www-data";

