ALTER TABLE document_topic	ADD CONSTRAINT doc_id_fk		FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE document_topic	ADD CONSTRAINT topic_num_fk		FOREIGN KEY (topic_num)			REFERENCES topic(topic_num);
