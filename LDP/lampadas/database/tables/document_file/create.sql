CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL
				REFERENCES document(doc_id),
	filename		TEXT		NOT NULL,
	format_id		INT4
				REFERENCES format(format_id),

	PRIMARY KEY (doc_id, filename)
);
