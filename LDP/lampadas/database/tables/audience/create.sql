CREATE TABLE audience (
	audience_code		CHAR(12)	NOT NULL,
	audience_level		INT4		NOT NULL,
	audience_description	TEXT,

	PRIMARY KEY (audience_code)
);
