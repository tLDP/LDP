CREATE TABLE license
(
	license_code	CHAR(12)	NOT NULL,
	free		BOOLEAN		NOT NULL	DEFAULT False,
	sort_order	INT4		NOT NULL,

	PRIMARY KEY (license_code)
);
