CREATE TABLE page
(
	page_code		CHAR(20)	NOT NULL,
	section_code		CHAR(12),
	sort_order		INT4		NOT NULL DEFAULT 0,
	template_code		CHAR(12)	NOT NULL,
	data			CHAR(40),
	only_dynamic		BOOLEAN		DEFAULT False,
	only_registered		BOOLEAN		DEFAULT False,
	only_admin		BOOLEAN		DEFAULT False,
	only_sysadmin		BOOLEAN		DEFAULT False,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (page_code)
);
