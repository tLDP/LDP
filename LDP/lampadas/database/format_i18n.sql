DROP TABLE format_i18n;

CREATE TABLE format_i18n
(
	format			CHAR(12)	NOT NULL,
	lang			CHAR(2)		NOT NULL,
	format_name		TEXT		NOT NULL,

	PRIMARY KEY (format, lang)
);
