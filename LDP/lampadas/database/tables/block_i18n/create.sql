CREATE TABLE block_i18n
(
	block_code	CHAR(12)	NOT NULL,
	lang		CHAR(2)		NOT NULL,
	block		TEXT		NOT NULL,

	PRIMARY KEY (block_code, lang)
);
