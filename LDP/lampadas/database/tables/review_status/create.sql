CREATE TABLE review_status
(
	review_status_code	CHAR		NOT NULL,
	sort_order		INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (review_status_code)
);

CREATE INDEX review_status_upd_idx ON review_status (updated);
CREATE INDEX review_status_ctd_idx ON review_status (created);
