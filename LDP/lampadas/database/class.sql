DROP TABLE class;

CREATE TABLE class
(
	class			CHAR(12)	NOT NULL,
	class_name		TEXT		NOT NULL,

	PRIMARY KEY (class)
);

GRANT SELECT ON class TO "www-data";
