CREATE TABLE section_i18n
(
	section_code		CHAR(20)	NOT NULL	REFERENCES section(section_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	section_name		TEXT		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (section_code, lang)
);
