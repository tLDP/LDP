CREATE TABLE review_status
(
	review_status_code	CHAR		NOT NULL,
	sort_order		INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (review_status_code)
);
