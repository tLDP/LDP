CREATE TABLE document_user (
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	username		CHAR(40)	NOT NULL	REFERENCES username(username),
	role_code		CHAR(12)	NOT NULL	REFERENCES role(role_code),
	email			TEXT,
	active			BOOLEAN		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id, username, role_code)
);

CREATE INDEX document_user_upd_idx ON document_user (updated);
CREATE INDEX document_user_ctd_idx ON document_user (created);
