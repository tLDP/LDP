CREATE TABLE block_i18n
(
	block_code	CHAR(12)	NOT NULL
			REFERENCES block(block_code),
	lang		CHAR(2)		NOT NULL
			REFERENCES language(isocode),
	block		TEXT		NOT NULL,

	PRIMARY KEY (block_code, lang)
);
