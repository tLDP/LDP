CREATE TABLE document_error
(
	doc_id			INT4		NOT NULL
				REFERENCES document(doc_id),
	err_id			INT4		NOT NULL
);
