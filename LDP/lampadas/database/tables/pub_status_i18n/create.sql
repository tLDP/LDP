CREATE TABLE pub_status_i18n
(
	pub_status_code		CHAR		NOT NULL	REFERENCES pub_status(pub_status_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	pub_status_name		TEXT,
	pub_status_desc		TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),
	
	PRIMARY KEY (pub_status_code, lang)
);

CREATE INDEX pub_status_i18n_upd_idx ON pub_status_i18n (updated);
CREATE INDEX pub_status_i18n_ctd_idx ON pub_status_i18n (created);
