CREATE TABLE page
(
	page_code	CHAR(20)	NOT NULL,
	section_code	CHAR(12),
	sort_order	INT4		NOT NULL,
	template_code	CHAR(12)	NOT NULL,

	PRIMARY KEY (page_code)
);
