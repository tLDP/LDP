DROP TABLE language;

CREATE TABLE language
(
	isocode			CHAR(2),
	supported		BOOLEAN DEFAULT False,

	PRIMARY KEY (isocode)
);

