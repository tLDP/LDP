DROP TABLE notes;

CREATE TABLE notes (
	doc_id		INT4	NOT NULL,
	date_entered	TIMESTAMP NOT NULL DEFAULT timestamp(date 'today'),
	notes		TEXT,
	username	CHAR(12)
);

ALTER TABLE notes
ADD CONSTRAINT doc_id_fk
FOREIGN KEY (doc_id)
REFERENCES document(doc_id);

GRANT SELECT on notes to webuser;
GRANT INSERT on notes to webuser;
