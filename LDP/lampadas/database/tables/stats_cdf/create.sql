CREATE TABLE stats_cdf (
	date_entered		CHAR(10)	NOT NULL,
	class			CHAR(12)	NOT NULL,
	dtd			CHAR(12)	NOT NULL,
	format			CHAR(12)	NOT NULL,
	doc_cnt_cdf		INT4		NOT NULL,
	created			TIMESTAMP	NOT NULL	DEFAULT now(),
	updated			TIMESTAMP	NOT NULL	DEFAULT now()
);

CREATE INDEX stats_cdf_upd_idx ON stats_cdf (updated);
CREATE INDEX stats_cdf_ctd_idx ON stats_cdf (created);
