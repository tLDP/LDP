DROP TABLE maintainer;

CREATE TABLE maintainer (
	maintainer_id		INT4	NOT NULL,
	maintainer_name		TEXT,
	email			TEXT,

	PRIMARY KEY (maintainer_id)	
);
