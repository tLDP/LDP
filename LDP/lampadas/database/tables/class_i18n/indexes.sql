ALTER TABLE class_i18n		ADD CONSTRAINT class_id_fk		FOREIGN KEY (class_id)			REFERENCES class(class_id);
ALTER TABLE class_i18n		ADD CONSTRAINT class_lang_fk		FOREIGN KEY (lang)			REFERENCES language(isocode);
