CREATE TABLE format_i18n
(
	format_code		CHAR(20)	NOT NULL	REFERENCES format(format_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	format_name		TEXT		NOT NULL,
	format_desc		TEXT,

	PRIMARY KEY (format_code, lang)
);
