DROP TABLE string_i18n;

CREATE TABLE string_i18n
(
	string_id		INT4		NOT NULL,
	lang			CHAR(2)		NOT NULL,
	string			TEXT		NOT NULL,

	PRIMARY KEY (string_id, lang)
);
