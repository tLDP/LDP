CREATE TABLE format_i18n
(
	format_id		INT4		NOT NULL	REFERENCES format(format_id),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	format_name		TEXT		NOT NULL,
	format_desc		TEXT,

	PRIMARY KEY (format_id, lang)
);
