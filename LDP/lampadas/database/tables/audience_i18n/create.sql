CREATE TABLE audience_i18n (
	audience_code	CHAR	NOT NULL	REFERENCES audience(audience_code),
	lang		CHAR	NOT NULL	REFERENCES language(isocode),
	audience_name	TEXT	NOT NULL,
	audience_desc	TEXT,

	PRIMARY KEY (audience_code, lang)
);
