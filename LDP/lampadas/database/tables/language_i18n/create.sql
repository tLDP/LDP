CREATE TABLE language_i18n
(
	lang_code		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	lang_name		CHAR(60),

	PRIMARY KEY (lang_code, lang)
);
