DROP TABLE document;

CREATE TABLE document
(
	doc_id			INT4		NOT NULL,
	title			TEXT		NOT NULL,
	class			CHAR(12),
	format			CHAR(12),
	dtd			CHAR(12),
	dtd_version		CHAR(12),
	version			CHAR(12),
	last_update		DATE,
	URL			TEXT,
	ISBN			TEXT,
	pub_status		CHAR,
	review_status		CHAR,
	tickle_date		DATE,
	pub_date		DATE,
	ref_url			TEXT,
	tech_review_status	CHAR,
	maintained		BOOLEAN	DEFAULT False,
	license			CHAR(12),
	abstract		TEXT,
	rating			REAL,

	PRIMARY KEY (doc_id)
);
