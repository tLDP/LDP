CREATE TABLE document_audience (
	audience		CHAR(12)	NOT NULL,
	doc_id			INT4		NOT NULL,
	
	PRIMARY KEY (doc_id, audience)
);
