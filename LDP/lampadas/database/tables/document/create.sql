CREATE TABLE document
(
	doc_id			INT4		NOT NULL,
	lang			CHAR(2)				REFERENCES language(lang_code),
	title			TEXT,
	short_title		TEXT,
	type_code		CHAR(20)			REFERENCES type(type_code),
	format_code		CHAR(20)			REFERENCES format(format_code),
	dtd_code		CHAR(12)			REFERENCES dtd(dtd_code),
	dtd_version		CHAR(12),
	version			CHAR(12),
	last_update		DATE,
	isbn			TEXT,
	pub_status_code		CHAR				REFERENCES pub_status(pub_status_code),
	review_status_code	CHAR				REFERENCES review_status(review_status_code),
	tickle_date		DATE,
	pub_date		TEXT,
	tech_review_status_code	CHAR				REFERENCES review_status(review_status_code),
	maintained		BOOLEAN		DEFAULT False,
	maintainer_wanted	BOOLEAN		DEFAULT False,
	license_code		CHAR(12)			REFERENCES license(license_code),
	license_version		CHAR(12),
	copyright_holder	TEXT,
	abstract		TEXT,
	short_desc		TEXT,
	rating			REAL,
	sk_seriesid		CHAR(36)	NOT NULL,
	replaced_by_id		INT4,
	lint_time		TIMESTAMP,
	pub_time		TIMESTAMP,
	mirror_time		TIMESTAMP,
	first_pub_date		TEXT,
	encoding		CHAR(12),
	deleted			BOOLEAN		DEFAULT False,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (doc_id)
);

CREATE INDEX document_upd_idx ON document (updated);
CREATE INDEX document_ctd_idx ON document (created);
