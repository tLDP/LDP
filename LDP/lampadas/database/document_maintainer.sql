DROP TABLE document_maintainer;

CREATE TABLE document_maintainer
(
	doc_id			INT4		NOT NULL,
	maintainer_id		INT4		NOT NULL,
	role			CHAR(12)	NOT NULL,
	active			BOOLEAN		NOT NULL,
	email			TEXT,
	email_private		TEXT,

	PRIMARY KEY (doc_id, maintainer_id, role)
);


ALTER TABLE document_maintainer
ADD CONSTRAINT doc_id_fk
FOREIGN KEY (doc_id)
REFERENCES document(doc_id);

ALTER TABLE document_maintainer
ADD CONSTRAINT maintainer_id_fk
FOREIGN KEY (maintainer_id)
REFERENCES maintainer(maintainer_id);

ALTER TABLE document_maintainer
ADD CONSTRAINT role_fk
FOREIGN KEY (role)
REFERENCES role(role);

GRANT SELECT on document_maintainer to webuser;
GRANT UPDATE on document_maintainer to webuser;
GRANT DELETE on document_maintainer to webuser;
