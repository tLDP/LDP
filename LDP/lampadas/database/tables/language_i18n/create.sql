CREATE TABLE language_i18n
(
	isocode			CHAR(2)		NOT NULL
				REFERENCES language(isocode),
	lang			CHAR(2)		NOT NULL
				REFERENCES language(isocode),
	language_name		CHAR(60),

	PRIMARY KEY (isocode, lang)
);
