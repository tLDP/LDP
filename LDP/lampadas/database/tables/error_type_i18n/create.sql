CREATE TABLE error_type_i18n
(
	err_type_code		CHAR(12)	NOT NULL	REFERENCES error_type(err_type_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	err_type_name		TEXT		NOT NULL,
	err_type_desc		TEXT,

	PRIMARY KEY (err_type_code, lang)
);
