CREATE TABLE document_notes (
	note_id			INT4		NOT NULL,
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	notes			TEXT,
	creator			CHAR(40)	NOT NULL	REFERENCES username(username),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (note_id)
);

CREATE INDEX document_notes_upd_idx ON document_notes (updated);
CREATE INDEX document_notes_ctd_idx ON document_notes (created);
