CREATE TABLE error_i18n
(
	err_id			INT4		NOT NULL	REFERENCES error(err_id),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	err_name		TEXT		NOT NULL,
	err_desc		TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (err_id, lang)
);
