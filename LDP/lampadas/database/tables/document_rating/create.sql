CREATE TABLE document_rating
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	username		CHAR(40)	NOT NULL	REFERENCES username(username),
	rating			INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id, username)
);

CREATE INDEX document_rating_upd_idx ON document_rating (updated);
CREATE INDEX document_rating_ctd_idx ON document_rating (created);
