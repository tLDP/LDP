CREATE TABLE pub_status_i18n
(
	pub_status		CHAR		NOT NULL
				REFERENCES pub_status(pub_status),
	lang			CHAR(2)		NOT NULL
				REFERENCES language(isocode),
	pub_status_name		TEXT,
	pub_status_desc		TEXT,
	
	PRIMARY KEY (pub_status, lang)
);
