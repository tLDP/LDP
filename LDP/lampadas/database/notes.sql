DROP TABLE notes;

CREATE TABLE notes (
	doc_id		INT4	NOT NULL,
	date_entered	TIMESTAMP NOT NULL DEFAULT now(),
	notes		TEXT,
	username	CHAR(20)
);
