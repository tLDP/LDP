CREATE TABLE page
(
	page_code	CHAR(20)	NOT NULL,
	section_code	CHAR(12),
	sort_order	INT4		NOT NULL,
	template_code	CHAR(12)	NOT NULL,
	data		CHAR(40),
	only_dynamic	BOOLEAN		DEFAULT False,
	only_registered	BOOLEAN		DEFAULT False,
	only_admin	BOOLEAN		DEFAULT False,
	only_sysadmin	BOOLEAN		DEFAULT False,

	PRIMARY KEY (page_code)
);
