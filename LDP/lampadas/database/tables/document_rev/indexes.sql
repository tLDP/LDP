ALTER TABLE document_rev	ADD CONSTRAINT doc_id_fk		FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
