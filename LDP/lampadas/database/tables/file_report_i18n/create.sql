CREATE TABLE file_report_i18n
(
	report_code		CHAR(20)	NOT NULL,
	lang			CHAR(2)		REFERENCES language(lang_code),
	report_name		TEXT,
	report_desc		TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (report_code, lang)
);

CREATE INDEX file_report_i18n_upd_idx ON file_report_i18n (updated);
CREATE INDEX file_report_i18n_ctd_idx ON file_report_i18n (created);
