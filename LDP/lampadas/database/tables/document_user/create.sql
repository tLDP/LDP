CREATE TABLE document_user (
	doc_id		INT4		NOT NULL
			REFERENCES document(doc_id),
	user_id		INT4		NOT NULL
			REFERENCES username(user_id),
	role		CHAR(12)	NOT NULL
			REFERENCES role(role),
	email		TEXT,
	active		BOOLEAN		NOT NULL,

	PRIMARY KEY (doc_id, user_id, role)
);
