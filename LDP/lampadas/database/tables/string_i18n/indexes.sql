ALTER TABLE string_i18n		ADD CONSTRAINT string_lang_fk		FOREIGN KEY (lang)			REFERENCES language(isocode);
