CREATE TABLE format_i18n
(
	format_id		INT4		NOT NULL,
	lang			CHAR(2)		NOT NULL,
	format_name		TEXT		NOT NULL,
	format_desc		TEXT,

	PRIMARY KEY (format_id, lang)
);
