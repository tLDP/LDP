CREATE TABLE subtopic_i18n
(
	subtopic_code		CHAR(20)	NOT NULL	REFERENCES subtopic(subtopic_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(isocode),
	subtopic_name		TEXT		NOT NULL,
	subtopic_desc		TEXT,

	PRIMARY KEY (subtopic_code, lang)
);
