DROP TABLE volunteer;

CREATE TABLE volunteer (
	volunteer_id	INT4	NOT NULL,
	name		TEXT,
	email		TEXT,
	role		CHAR(10),

	PRIMARY KEY (volunteer_id)
);

GRANT ALL ON volunteer TO "www-data";

