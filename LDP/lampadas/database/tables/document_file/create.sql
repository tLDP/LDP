CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	filename		TEXT		NOT NULL,
	format_code		CHAR(20)			REFERENCES format(format_code),

	PRIMARY KEY (doc_id, filename)
);
