CREATE TABLE role_i18n(
	role		CHAR(12)	NOT NULL	REFERENCES role(role),
	lang		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	role_name	TEXT		NOT NULL,
	role_desc	TEXT,

	PRIMARY KEY (role, lang)
);
