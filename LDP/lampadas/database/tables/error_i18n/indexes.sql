ALTER TABLE error_i18n		ADD CONSTRAINT err_id_fk		FOREIGN KEY (err_id)			REFERENCES error(err_id);
ALTER TABLE error_i18n		ADD CONSTRAINT lang_fk			FOREIGN KEY (lang)			REFERENCES language(isocode);
