CREATE TABLE collection
(
	collection_code		CHAR(20)	NOT NULL,
	sort_order		INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (collection_code)
);

CREATE INDEX collection_upd_idx ON collection (updated);
CREATE INDEX collection_ctd_idx ON collection (created);
