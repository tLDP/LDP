CREATE TABLE review_status_i18n
(
	review_status		CHAR		NOT NULL	REFERENCES review_status(review_status),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	review_status_name	TEXT,
	review_status_desc	TEXT,
	
	PRIMARY KEY (review_status, lang)
);
