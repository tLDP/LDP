CREATE TABLE document_topic
(
	doc_id			INT4		NOT NULL
				REFERENCES document(doc_id),
	topic_num		INT4		NOT NULL
				REFERENCES topic(topic_num),
	subtopic_num		INT4		NOT NULL,

	PRIMARY KEY (doc_id, topic_num, subtopic_num)
);
