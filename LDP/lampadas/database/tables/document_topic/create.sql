CREATE TABLE document_topic
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	subtopic_code		CHAR(20)	NOT NULL	REFERENCES subtopic(subtopic_code),

	PRIMARY KEY (doc_id, subtopic_code)
);
