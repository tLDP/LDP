CREATE TABLE document_wiki (
	doc_id		INT4		NOT NULL	REFERENCES document(doc_id),
	revision	INT4		NOT NULL,
	date_entered	TIMESTAMP	NOT NULL DEFAULT now(),
	wiki		TEXT,
	notes		CHAR(256),
	username	CHAR(20)	NOT NULL	REFERENCES username(username),

	PRIMARY KEY (doc_id, revision)
);
