CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	filename		TEXT		NOT NULL	REFERENCES sourcefile(filename),
	top			BOOLEAN		DEFAULT False,

	PRIMARY KEY (doc_id, filename)
);
