ALTER TABLE string_i18n		ADD CONSTRAINT string_code_fk		FOREIGN KEY (string_code)		REFERENCES string(string_code);
ALTER TABLE string_i18n		ADD CONSTRAINT string_lang_fk		FOREIGN KEY (lang)			REFERENCES language(isocode);
