CREATE TABLE type_i18n
(
	type_code		CHAR(20)	NOT NULL	REFERENCES type(type_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	type_name		TEXT		NOT NULL,
	type_desc		TEXT		NOT NULL,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (type_code, lang)
);
