ALTER TABLE topic_i18n		ADD CONSTRAINT topic_num_fk		FOREIGN KEY (topic_num)			REFERENCES topic(topic_num);
ALTER TABLE topic_i18n		ADD CONSTRAINT lang_fk			FOREIGN KEY (lang)			REFERENCES language(isocode);
