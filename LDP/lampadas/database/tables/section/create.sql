CREATE TABLE section
(
	section_code		CHAR(20)	NOT NULL,
	sort_order		INT4		NOT NULL,
	only_dynamic		BOOLEAN		DEFAULT False,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (section_code)
);
