CREATE TABLE doc_vote
(
	doc_id		INT4		NOT NULL
			REFERENCES document(doc_id),
	user_id		INT4		NOT NULL
			REFERENCES username(user_id),
	date_entered	TIMESTAMP	NOT NULL DEFAULT now(),
	vote		INT4		NOT NULL,

	PRIMARY KEY (doc_id, user_id)
);
