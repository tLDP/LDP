CREATE TABLE file_report
(
	report_code		CHAR(20)	NOT NULL,
	only_cvs		BOOLEAN		DEFAULT False,
	command			TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),
	
	PRIMARY KEY (report_code)
);
