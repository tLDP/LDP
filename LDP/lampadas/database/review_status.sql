DROP TABLE review_status;

CREATE TABLE review_status
(
	review_status		CHAR		NOT NULL,
	review_status_name	TEXT,

	PRIMARY KEY (review_status)
);

GRANT SELECT ON review_status TO "www-data";

