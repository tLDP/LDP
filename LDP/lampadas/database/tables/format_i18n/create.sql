CREATE TABLE format_i18n
(
	format_code		CHAR(20)	NOT NULL	REFERENCES format(format_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	format_name		TEXT		NOT NULL,
	format_desc		TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (format_code, lang)
);

CREATE INDEX format_i18n_upd_idx ON format_i18n (updated);
CREATE INDEX format_i18n_ctd_idx ON format_i18n (created);
