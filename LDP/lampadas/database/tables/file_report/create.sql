CREATE TABLE file_report
(
	report_code		CHAR(20)	NOT NULL,
	only_cvs		BOOLEAN		DEFAULT False,
	command			TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),
	
	PRIMARY KEY (report_code)
);

CREATE INDEX file_report_upd_idx ON file_report (updated);
CREATE INDEX file_report_ctd_idx ON file_report (created);
