CREATE TABLE string_i18n
(
	string_code		CHAR(40)	NOT NULL	REFERENCES string(string_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	string			TEXT		NOT NULL,
	version			CHAR(12)	NOT NULL	DEFAULT '1.0',
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (string_code, lang)
);
