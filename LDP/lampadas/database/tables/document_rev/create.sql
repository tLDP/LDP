CREATE TABLE document_rev
(
	rev_id			INT4		NOT NULL,
	doc_id			INT4		NOT NULL
				REFERENCES document(doc_id),
	version			CHAR(12)	NOT NULL,
	pub_date		DATE,
	initials		CHAR(3)		NOT NULL,
	notes			TEXT,

	PRIMARY KEY (doc_id, rev_id)
);
