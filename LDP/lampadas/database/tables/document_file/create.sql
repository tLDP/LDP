CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	filename		TEXT		NOT NULL	REFERENCES sourcefile(filename),
	top			BOOLEAN		DEFAULT False,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id, filename)
);
