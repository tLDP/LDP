CREATE TABLE document_collection
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	collection_code		CHAR(20)	NOT NULL	REFERENCES collection(collection_code),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),
	
	PRIMARY KEY (doc_id, collection_code)
);

CREATE INDEX document_collection_upd_idx ON document_collection (updated);
CREATE INDEX document_collection_ctd_idx ON document_collection (created);
