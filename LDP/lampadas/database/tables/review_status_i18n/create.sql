CREATE TABLE review_status_i18n
(
	review_status_code	CHAR		NOT NULL	REFERENCES review_status(review_status_code),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	review_status_name	TEXT,
	review_status_desc	TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),
	
	PRIMARY KEY (review_status_code, lang)
);
