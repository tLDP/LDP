ALTER TABLE document_file	ADD CONSTRAINT doc_id_fk		FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE document_file	ADD CONSTRAINT format_id_fk		FOREIGN KEY (format_id)			REFERENCES format(format_id);
