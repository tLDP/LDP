DROP TABLE doc_vote;

CREATE TABLE doc_vote
(
	doc_id		INT4		NOT NULL,
	username	CHAR(12)	NOT NULL,
	date_entered	TIMESTAMP	NOT NULL DEFAULT timestamp(date 'today'),
	vote		INT4		NOT NULL,

	PRIMARY KEY (doc_id, username)
);
