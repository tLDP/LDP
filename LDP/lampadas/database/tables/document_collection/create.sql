CREATE TABLE document_collection
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	collection_code		CHAR(20)	NOT NULL	REFERENCES collection(collection_code),

	PRIMARY KEY (doc_id, collection_code)
);
