CREATE TABLE audience_i18n (
	audience_code	CHAR	NOT NULL	REFERENCES audience(audience_code),
	lang		CHAR(2)	NOT NULL	REFERENCES language(lang_code),
	audience_name	TEXT	NOT NULL,
	audience_desc	TEXT,

	PRIMARY KEY (audience_code, lang)
);
