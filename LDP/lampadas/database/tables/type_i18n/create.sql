CREATE TABLE type_i18n
(
	type_code	CHAR(20)	NOT NULL	REFERENCES type(type_code),
	lang		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	type_name	CHAR(20)	NOT NULL,
	type_desc	TEXT		NOT NULL,

	PRIMARY KEY (type_code, lang)
);
