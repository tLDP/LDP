CREATE TABLE class_i18n
(
	class_code	CHAR(20)	NOT NULL	REFERENCES class(class_code),
	lang		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	class_name	CHAR(20)	NOT NULL,
	class_desc	TEXT		NOT NULL,

	PRIMARY KEY (class_code, lang)
);
