CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	filename		TEXT		NOT NULL	REFERENCES sourcefile(filename),
	top			BOOLEAN		DEFAULT False,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id, filename)
);

CREATE INDEX document_file_doc_idx  ON document_file (doc_id);
CREATE INDEX document_file_file_idx ON document_file (filename);
CREATE INDEX document_file_upd_idx  ON document_file (updated);
CREATE INDEX document_file_ctd_idx  ON document_file (created);
