DROP TABLE class_i18n;

CREATE TABLE class_i18n
(
	class_id		INT4		NOT NULL,
	lang			CHAR(2)		NOT NULL,
	class_name		CHAR(20)	NOT NULL,
	class_description	TEXT		NOT NULL,

	PRIMARY KEY (class_id, lang)
);
