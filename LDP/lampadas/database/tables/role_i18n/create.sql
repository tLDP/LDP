CREATE TABLE role_i18n(
	role_code		CHAR(12)	NOT NULL	REFERENCES role(role_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	role_name		TEXT		NOT NULL,
	role_desc		TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (role_code, lang)
);

CREATE INDEX role_i18n_upd_idx ON role_i18n (updated);
CREATE INDEX role_i18n_ctd_idx ON role_i18n (created);
