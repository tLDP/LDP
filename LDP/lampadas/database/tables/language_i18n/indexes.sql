ALTER TABLE language_i18n	ADD CONSTRAINT language_fk		FOREIGN KEY (isocode)			REFERENCES language(isocode);
ALTER TABLE language_i18n	ADD CONSTRAINT language_lang_fk		FOREIGN KEY (lang)			REFERENCES language(isocode);
