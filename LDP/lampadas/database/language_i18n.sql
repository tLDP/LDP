DROP TABLE language_i18n;

CREATE TABLE language_i18n
(
	isocode			CHAR(2),
	lang			CHAR(2),
	language_name		CHAR(60),

	PRIMARY KEY (isocode, lang)
);

