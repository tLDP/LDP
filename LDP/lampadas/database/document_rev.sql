DROP TABLE document_rev;

CREATE TABLE document_rev
(
	rev_id			INT4		NOT NULL,
	doc_id			INT4		NOT NULL,
	version			CHAR(12)	NOT NULL,
	pub_date		DATE,
	initials		CHAR(3)		NOT NULL,
	notes			TEXT,

	PRIMARY KEY (doc_id, rev_id)
);

ALTER TABLE document_rev
ADD CONSTRAINT doc_id_fk
FOREIGN KEY (doc_id)
REFERENCES document(doc_id);

GRANT ALL ON document_rev TO "www-data";
GRANT SELECT on document_rev to root;
