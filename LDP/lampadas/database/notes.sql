DROP TABLE notes;

CREATE TABLE notes (
	doc_id		INT4	NOT NULL,
	date_entered	TIMESTAMP NOT NULL DEFAULT now(),
	notes		TEXT,
	username	CHAR(12)
);

ALTER TABLE notes
ADD CONSTRAINT doc_id_fk
FOREIGN KEY (doc_id)
REFERENCES document(doc_id);

GRANT ALL ON notes TO "www-data";

