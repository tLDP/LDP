CREATE TABLE document_wiki (
	doc_id		INT4		NOT NULL
			REFERENCES document(doc_id),
	revision	INT4		NOT NULL,
	date_entered	TIMESTAMP	NOT NULL DEFAULT now(),
	wiki		TEXT,
	notes		CHAR(256),
	user_id		INT4		NOT NULL
			REFERENCES username(user_id),

	PRIMARY KEY (doc_id, revision)
);
