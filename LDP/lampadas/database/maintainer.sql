DROP TABLE maintainer;

CREATE TABLE maintainer (
	maintainer_id		INT4	NOT NULL,
	maintainer_name		TEXT,
	email			TEXT,

	PRIMARY KEY (maintainer_id)	
);

GRANT ALL ON maintainer TO "www-data";
GRANT SELECT ON maintainer TO root;
