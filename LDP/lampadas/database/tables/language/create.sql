CREATE TABLE language
(
	lang_code		CHAR(2)		NOT NULL,
	supported		BOOLEAN		NOT NULL	DEFAULT False,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (lang_code)
);

