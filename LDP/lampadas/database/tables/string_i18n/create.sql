CREATE TABLE string_i18n
(
	string_code	CHAR(20)	NOT NULL	REFERENCES string(string_code),
	lang		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	string		TEXT		NOT NULL,

	PRIMARY KEY (string_code, lang)
);
