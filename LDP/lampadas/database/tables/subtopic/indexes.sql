ALTER TABLE subtopic		ADD CONSTRAINT topic_num_fk		FOREIGN KEY (topic_num)			REFERENCES topic(topic_num);
