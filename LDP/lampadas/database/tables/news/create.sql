CREATE TABLE news
(
	news_id		INT4	NOT NULL,
	pub_date	DATE	NOT NULL	DEFAULT now(),

	PRIMARY KEY (news_id)
);
