DROP TABLE stats_CDF;

CREATE TABLE stats_CDF (
	date_entered	CHAR(10)	NOT NULL,
	class		CHAR(12)	NOT NULL,
	dtd		CHAR(12)	NOT NULL,
	format		CHAR(12)	NOT NULL,
	doc_cnt_CDF	INT4		NOT NULL
);

GRANT SELECT ON stats_CDF to "www-data";
GRANT ALL ON stats_CDF to root;
