CREATE TABLE role_i18n(
	role_code	CHAR(12)	NOT NULL	REFERENCES role(role_code),
	lang		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	role_name	TEXT		NOT NULL,
	role_desc	TEXT,

	PRIMARY KEY (role_code, lang)
);
