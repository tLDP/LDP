CREATE TABLE section_i18n
(
	section_code	CHAR(20)	NOT NULL	REFERENCES section(section_code),
	lang		CHAR(2)		NOT NULL,
	section_name	TEXT		NOT NULL,

	PRIMARY KEY (section_code, lang)
);
