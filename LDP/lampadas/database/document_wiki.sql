DROP TABLE document_wiki;

CREATE TABLE document_wiki (
	doc_id		INT4		NOT NULL,
	revision	INT4		NOT NULL,
	date_entered	TIMESTAMP	NOT NULL DEFAULT now(),
	wiki		TEXT,
	notes		CHAR(256),
	user_id		INT4		NOT NULL,

	PRIMARY KEY (doc_id, revision)
);
