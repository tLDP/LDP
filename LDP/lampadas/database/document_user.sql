CREATE TABLE document_user (
	doc_id		INT4		NOT NULL,
	user_id		INT4		NOT NULL,
	role		CHAR(12)	NOT NULL,
	email		TEXT,
	active		BOOLEAN		NOT NULL,

	PRIMARY KEY (doc_id, user_id, role)
);
