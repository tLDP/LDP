CREATE TABLE topic
(
	parent_code	CHAR(20),
	topic_code	CHAR(20)	NOT NULL,
	sort_order	INT4		NOT NULL,

	PRIMARY KEY (topic_code)
);
