DROP TABLE audience;

CREATE TABLE audience (
	audience		CHAR(12)	NOT NULL,
	audience_level		INT4		NOT NULL,
	audience_description	TEXT,

	PRIMARY KEY (audience)	
);

GRANT SELECT ON audience TO "www-data";
