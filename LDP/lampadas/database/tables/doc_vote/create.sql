CREATE TABLE doc_vote
(
	doc_id			INT4		NOT NULL	REFERENCES document(doc_id),
	username		CHAR(40)	NOT NULL	REFERENCES username(username),
	vote			INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id, username)
);
