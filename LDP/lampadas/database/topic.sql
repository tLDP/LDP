DROP TABLE topic;

CREATE TABLE topic
(
	topic_num		INT4		NOT NULL,
	topic_name		TEXT		NOT NULL,
	topic_description	TEXT,
	

	PRIMARY KEY (topic_num)
);

GRANT ALL on topic to webuser;
