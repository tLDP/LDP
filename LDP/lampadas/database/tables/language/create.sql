CREATE TABLE language
(
	lang_code		CHAR(2)		NOT NULL,
	supported		BOOLEAN		NOT NULL	DEFAULT False,
	encoding		CHAR(12),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (lang_code)
);

CREATE INDEX language_upd_idx ON language (updated);
CREATE INDEX language_ctd_idx ON language (created);
