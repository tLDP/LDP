CREATE TABLE file_report
(
	report_code	CHAR(20)	NOT NULL,
	only_cvs	BOOLEAN		DEFAULT False,
	command		TEXT,

	PRIMARY KEY (report_code)
);
