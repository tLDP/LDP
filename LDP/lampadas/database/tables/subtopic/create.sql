CREATE TABLE subtopic
(
	subtopic_code		CHAR(20)	NOT NULL,
	subtopic_num		INT4		NOT NULL,
	topic_code		CHAR(20)	NOT NULL	REFERENCES topic(topic_code),

	PRIMARY KEY (subtopic_code)
);
