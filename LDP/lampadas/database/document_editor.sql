DROP TABLE document_editor;

CREATE TABLE document_editor
(
	doc_id			INT4		NOT NULL,
	editor_id		INT4		NOT NULL,
	editor_role		CHAR(12)	NOT NULL,
	active			BOOLEAN		NOT NULL,

	PRIMARY KEY (doc_id, editor_id, editor_role)
);


ALTER TABLE document_editor
ADD CONSTRAINT doc_id_fk
FOREIGN KEY (doc_id)
REFERENCES document(doc_id);

ALTER TABLE document_editor
ADD CONSTRAINT editor_id_fk
FOREIGN KEY (editor_id)
REFERENCES editor(editor_id);

ALTER TABLE document_editor
ADD CONSTRAINT editor_role_fk
FOREIGN KEY (editor_role)
REFERENCES editor_role(editor_role);
