CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	filename		TEXT		NOT NULL	UNIQUE,
	top			BOOLEAN		DEFAULT False,
	format_code		CHAR(20)			REFERENCES format(format_code),
	filesize		INT4,
	filemode		CHAR(20),
	modified		TIMESTAMP,

	PRIMARY KEY (doc_id, filename)
);
