DROP TABLE document_file;

CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL,
	filename		CHAR(60)	NOT NULL,

	PRIMARY KEY (doc_id, filename)
);
