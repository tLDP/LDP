CREATE TABLE topic
(
	parent_code		CHAR(20),
	topic_code		CHAR(20)	NOT NULL,
	sort_order		INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now(),

	PRIMARY KEY (topic_code)
);

CREATE INDEX topic_upd_idx ON topic (updated);
CREATE INDEX topic_ctd_idx ON topic (created);
