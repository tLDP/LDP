ALTER TABLE format_i18n		ADD CONSTRAINT format_id_fk		FOREIGN KEY (format_id)			REFERENCES format(format_id);
ALTER TABLE format_i18n		ADD CONSTRAINT format_lang_fk		FOREIGN KEY (lang)			REFERENCES language(isocode);
