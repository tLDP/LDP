DROP TABLE maintainer_notes;

CREATE TABLE maintainer_notes (
	maintainer_id	INT4	NOT NULL,
	date_entered	TIMESTAMP NOT NULL DEFAULT timestamp(date 'today'),
	notes		TEXT,
	username	CHAR(12)
);

ALTER TABLE maintainer_notes
ADD CONSTRAINT maintainer_id_fk
FOREIGN KEY (maintainer_id)
REFERENCES maintainer(maintainer_id);

GRANT ALL ON notes TO "www-data";

