CREATE TABLE document_rev
(
	rev_id			INT4		NOT NULL,
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	version			CHAR(12)	NOT NULL,
	pub_date		DATE,
	initials		CHAR(3)		NOT NULL,
	notes			TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (rev_id)
);

CREATE INDEX document_rev_idx ON document_rev (doc_id);
CREATE INDEX document_rev_upd_idx ON document_rev (updated);
CREATE INDEX document_rev_ctd_idx ON document_rev (created);
