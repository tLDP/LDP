CREATE TABLE document_file
(
	doc_id			INT4		NOT NULL,
	filename		TEXT		NOT NULL,
	format_id		INT4,

	PRIMARY KEY (doc_id, filename)
);
