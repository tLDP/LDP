CREATE TABLE class_i18n
(
	class_id	INT4		NOT NULL	REFERENCES class(class_id),
	lang		CHAR(2)		NOT NULL	REFERENCES language(isocode),
	class_name	CHAR(20)	NOT NULL,
	class_desc	TEXT		NOT NULL,

	PRIMARY KEY (class_id, lang)
);
