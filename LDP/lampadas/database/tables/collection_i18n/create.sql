CREATE TABLE collection_i18n
(
	collection_code	CHAR(20)	NOT NULL	REFERENCES collection(collection_code),
	lang		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	collection_name	TEXT		NOT NULL,
	collection_desc	TEXT		NOT NULL,

	PRIMARY KEY (collection_code, lang)
);
