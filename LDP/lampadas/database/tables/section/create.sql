CREATE TABLE section
(
	section_code		CHAR(20)	NOT NULL,
	sort_order		INT4		NOT NULL,
	only_dynamic		BOOLEAN		DEFAULT False,
	only_registered		BOOLEAN		DEFAULT False,
	only_admin		BOOLEAN		DEFAULT False,
	only_sysadmin		BOOLEAN		DEFAULT False,

	PRIMARY KEY (section_code)
);
