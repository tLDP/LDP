CREATE TABLE language_i18n
(
	lang_code		CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	lang_name		CHAR(60),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (lang_code, lang)
);

CREATE INDEX language_i18n_upd_idx ON language_i18n (updated);
CREATE INDEX language_i18n_ctd_idx ON language_i18n (created);
