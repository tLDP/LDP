CREATE TABLE document_topic
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	topic_code		CHAR(20)	NOT NULL	REFERENCES topic(topic_code),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id, topic_code)
);

CREATE INDEX document_topic_upd_idx ON document_topic (updated);
CREATE INDEX document_topic_ctd_idx ON document_topic (created);
