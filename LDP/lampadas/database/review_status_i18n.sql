CREATE TABLE review_status_i18n
(
	review_status		CHAR		NOT NULL,
	lang			CHAR(2)		NOT NULL,
	review_status_name	TEXT,
	review_status_desc	TEXT,
	
	PRIMARY KEY (review_status, lang)
);
