DROP TABLE maintainer_notes;

CREATE TABLE maintainer_notes (
	maintainer_id	INT4	NOT NULL,
	date_entered	TIMESTAMP NOT NULL DEFAULT now(),
	notes		TEXT,
	username	CHAR(20)
);
