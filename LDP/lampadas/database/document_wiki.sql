DROP TABLE document_wiki;

CREATE TABLE document_wiki (
	doc_id		INT4	NOT NULL,
	revision	INT4	NOT NULL,
	date_entered	TIMESTAMP NOT NULL DEFAULT timestamp(date 'today'),
	wiki		TEXT,
	notes		CHAR(256),
	username	CHAR(12)
);

ALTER TABLE document_wiki
ADD CONSTRAINT doc_id_fk
FOREIGN KEY (doc_id)
REFERENCES document(doc_id);

GRANT ALL ON document_wiki TO "www-data";

