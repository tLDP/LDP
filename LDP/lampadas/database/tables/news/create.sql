CREATE TABLE news
(
	news_id			INT4		NOT NULL,
	pub_date		TIMESTAMP	NOT NULL	DEFAULT now(),
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (news_id)
);
