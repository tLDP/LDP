DROP TABLE page;

CREATE TABLE page
(
	page_code	CHAR(12)	NOT NULL,
	template_code	CHAR(12)	NOT NULL,

	PRIMARY KEY (page_code)
);
