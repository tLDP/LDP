ALTER TABLE notes		ADD CONSTRAINT doc_id_fk		FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE notes		ADD CONSTRAINT creator_id_fk		FOREIGN KEY (creator_id)		REFERENCES username(user_id);
