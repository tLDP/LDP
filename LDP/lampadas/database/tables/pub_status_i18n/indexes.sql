ALTER TABLE pub_status_i18n	ADD CONSTRAINT pub_status_fk		FOREIGN KEY (pub_status)		REFERENCES pub_status(pub_status);
ALTER TABLE pub_status_i18n	ADD CONSTRAINT pub_status_lang_fk	FOREIGN KEY (lang)			REFERENCES language(isocode);
