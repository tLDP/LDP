DROP TABLE document_topic;

CREATE TABLE document_topic
(
	doc_id			INT4		NOT NULL,
	topic_num		INT4		NOT NULL,
	subtopic_num		INT4		NOT NULL,

	PRIMARY KEY (doc_id, topic_num, subtopic_num)
);
