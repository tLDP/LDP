CREATE TABLE document
(
	doc_id			INT4		NOT NULL,
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	title			TEXT		NOT NULL,
	class_code		CHAR(20)	NOT NULL	REFERENCES class(class_code),
	format_id		INT4				REFERENCES format(format_id),
	dtd			CHAR(12)			REFERENCES dtd(dtd),
	dtd_version		CHAR(12),
	version			CHAR(12),
	last_update		DATE,
	URL			TEXT,
	ISBN			TEXT,
	pub_status		CHAR				REFERENCES pub_status(pub_status),
	review_status		CHAR				REFERENCES review_status(review_status),
	tickle_date		DATE,
	pub_date		DATE,
	ref_url			TEXT,
	tech_review_status	CHAR				REFERENCES review_status(review_status),
	maintained		BOOLEAN	DEFAULT False,
	license			CHAR(12)			REFERENCES license(license),
	abstract		TEXT,
	rating			REAL,
	sk_seriesid		CHAR(36),
	replaced_by_id		INT4,

	PRIMARY KEY (doc_id)
);
