CREATE TABLE notes (
	note_id			INT4		NOT NULL,
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	notes			TEXT,
	creator			CHAR(40)	NOT NULL	REFERENCES username(username),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id, created)
);
