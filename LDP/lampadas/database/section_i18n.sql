CREATE TABLE section_i18n
(
	section_code		CHAR(12)	NOT NULL,
	lang			CHAR(2)		NOT NULL,
	section_name		TEXT		NOT NULL,

	PRIMARY KEY (section_code, lang)
);
