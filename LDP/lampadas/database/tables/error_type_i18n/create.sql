CREATE TABLE error_type_i18n
(
	err_type_code		CHAR(12)	NOT NULL	REFERENCES error_type(err_type_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	err_type_name		TEXT		NOT NULL,
	err_type_desc		TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (err_type_code, lang)
);

CREATE INDEX error_type_i18n_upd_idx ON error_type_i18n (updated);
CREATE INDEX error_type_i18n_ctd_idx ON error_type_i18n (created);
