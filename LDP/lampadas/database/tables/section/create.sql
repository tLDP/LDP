CREATE TABLE section
(
	section_code		CHAR(20)	NOT NULL,
	sort_order		INT4		NOT NULL,
	only_dynamic		BOOLEAN		DEFAULT False,

	PRIMARY KEY (section_code)
);
