CREATE TABLE language
(
	lang_code		CHAR(2)		NOT NULL,
	supported		BOOLEAN		NOT NULL	DEFAULT False,

	PRIMARY KEY (lang_code)
);

