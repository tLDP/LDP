ALTER TABLE document_error	ADD CONSTRAINT doc_id_fk		FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
