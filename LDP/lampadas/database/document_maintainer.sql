DROP TABLE document_maintainer;

CREATE TABLE document_maintainer
(
	doc_id			INT4		NOT NULL,
	maintainer_id		INT4		NOT NULL,
	role			CHAR(12)	NOT NULL,
	active			BOOLEAN		NOT NULL,
	email			TEXT,
	email_private		TEXT,

	PRIMARY KEY (doc_id, maintainer_id, role)
);
