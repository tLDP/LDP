DROP TABLE editor;

CREATE TABLE editor (
	editor_id		INT4	NOT NULL,
	editor_name		TEXT,
	email			TEXT,
	notes			TEXT,

	PRIMARY KEY (editor_id)
);

GRANT ALL ON editor TO "www-data";

