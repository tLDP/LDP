CREATE TABLE pub_status_i18n
(
	pub_status		CHAR		NOT NULL,
	lang			CHAR(2)		NOT NULL,
	pub_status_name		TEXT,
	pub_status_desc		TEXT,
	
	PRIMARY KEY (pub_status, lang)
);
