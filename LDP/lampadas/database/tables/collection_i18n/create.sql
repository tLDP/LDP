CREATE TABLE collection_i18n
(
	collection_code		CHAR(20)	NOT NULL	REFERENCES collection(collection_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	collection_name		TEXT		NOT NULL,
	collection_desc		TEXT		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (collection_code, lang)
);

CREATE INDEX collection_i18n_upd_idx ON collection_i18n (updated);
CREATE INDEX collection_i18n_ctd_idx ON collection_i18n (created);
