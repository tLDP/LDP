CREATE TABLE license_i18n
(
	license_code		CHAR(12)	NOT NULL	REFERENCES license(license_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	license_short_name	CHAR(20)	NOT NULL,
	license_name		TEXT		NOT NULL,
	license_desc		TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (license_code, lang)
);
