DROP TABLE document;

CREATE TABLE document
(
	doc_id			INT4		NOT NULL,
	title			TEXT		NOT NULL,
	filename		TEXT,
	class			CHAR(12),
	format			CHAR(12),
	dtd			CHAR(12),
	dtd_version		CHAR(12),
	version			CHAR(12),
	last_update		DATE,
	URL			TEXT,
	ISBN			TEXT,
	pub_status		CHAR,
	author_status		CHAR,
	review_status		CHAR,
	tickle_date		DATE,
	pub_date		DATE,
	ref_url			TEXT,
	tech_review_status	CHAR,
	maintained		BOOLEAN	DEFAULT True,
	license_id		INT4,
	abstract		TEXT,

	PRIMARY KEY (doc_id)
);

ALTER TABLE document
ADD CONSTRAINT pub_status_fk
FOREIGN KEY  (pub_status)
REFERENCES pub_status(pub_status);

ALTER TABLE document
ADD CONSTRAINT review_status_fk
FOREIGN KEY  (review_status)
REFERENCES review_status(review_status);

ALTER TABLE document
ADD CONSTRAINT tech_review_status_fk
FOREIGN KEY  (tech_review_status)
REFERENCES review_status(review_status);

ALTER TABLE document
ADD CONSTRAINT class_fk
FOREIGN KEY (class)
REFERENCES class(class);

ALTER TABLE document
ADD CONSTRAINT format_fk
FOREIGN KEY (format)
REFERENCES format(format);

ALTER TABLE document
ADD CONSTRAINT dtd_fk
FOREIGN KEY (dtd)
REFERENCES dtd(dtd);
