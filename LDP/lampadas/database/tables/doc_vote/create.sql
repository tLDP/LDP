CREATE TABLE doc_vote
(
	doc_id		INT4		NOT NULL	REFERENCES document(doc_id),
	username	CHAR(20)	NOT NULL	REFERENCES username(username),
	date_entered	TIMESTAMP	NOT NULL DEFAULT now(),
	vote		INT4		NOT NULL,

	PRIMARY KEY (doc_id, username)
);
