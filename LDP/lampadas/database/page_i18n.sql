DROP TABLE page_i18n;

CREATE TABLE page_i18n
(
	page_code	CHAR(12)	NOT NULL,
	lang		CHAR(2)		NOT NULL,
	title		TEXT		NOT NULL,
	page		TEXT		NOT NULL,

	PRIMARY KEY (page_code, lang)
);
