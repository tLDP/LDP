DROP TABLE document_editor;

CREATE TABLE document_editor
(
	doc_id			INT4		NOT NULL,
	editor_id		INT4		NOT NULL,
	editor_role		CHAR(12)	NOT NULL,
	active			BOOLEAN		NOT NULL,

	PRIMARY KEY (doc_id, editor_id, editor_role)
);
