CREATE TABLE page_i18n
(
	page_code		CHAR(20)	NOT NULL	REFERENCES page(page_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	title			TEXT		NOT NULL,
	menu_name		TEXT		NOT NULL,
	page			TEXT		NOT NULL,
	version			CHAR(12)	NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (page_code, lang)
);
