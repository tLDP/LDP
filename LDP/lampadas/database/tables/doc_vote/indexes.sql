ALTER TABLE doc_vote		ADD CONSTRAINT doc_id_fk		FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE doc_vote		ADD CONSTRAINT user_id_fk		FOREIGN KEY (user_id)			REFERENCES username(user_id);
