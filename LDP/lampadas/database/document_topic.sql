DROP TABLE document_topic;

CREATE TABLE document_topic
(
	doc_id			INT4		NOT NULL,
	topic_num		INT4		NOT NULL,
	subtopic_num		INT4		NOT NULL,

	PRIMARY KEY (doc_id, topic_num, subtopic_num)
);

GRANT ALL on document_topic to webuser;

ALTER TABLE document_topic
ADD CONSTRAINT doc_id_fk
FOREIGN KEY (doc_id)
REFERENCES document(doc_id);

ALTER TABLE document_topic
ADD CONSTRAINT topic_num_fk
FOREIGN KEY (topic_num)
REFERENCES topic(topic_num);

ALTER TABLE document_topic
ADD CONSTRAINT subtopic_num_fk
FOREIGN KEY (subtopic_num)
REFERENCES subtopic(subtopic_num);

