ALTER TABLE document		ADD CONSTRAINT pub_status_fk	FOREIGN KEY (pub_status)		REFERENCES pub_status(pub_status);
ALTER TABLE document		ADD CONSTRAINT review_status_fk	FOREIGN KEY (review_status)		REFERENCES review_status(review_status);
ALTER TABLE document		ADD CONSTRAINT tech_status_fk	FOREIGN KEY (tech_review_status)	REFERENCES review_status(review_status);
ALTER TABLE document		ADD CONSTRAINT class_fk		FOREIGN KEY (class)			REFERENCES class(class);
ALTER TABLE document		ADD CONSTRAINT format_fk	FOREIGN KEY (format)			REFERENCES format(format);
ALTER TABLE document		ADD CONSTRAINT dtd_fk		FOREIGN KEY (dtd)			REFERENCES dtd(dtd);
ALTER TABLE document_rev	ADD CONSTRAINT doc_id_fk	FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE document_topic	ADD CONSTRAINT doc_id_fk	FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE document_topic	ADD CONSTRAINT topic_num_fk	FOREIGN KEY (topic_num)			REFERENCES topic(topic_num);
ALTER TABLE document_wiki	ADD CONSTRAINT doc_id_fk	FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE notes		ADD CONSTRAINT doc_id_fk	FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE subtopic		ADD CONSTRAINT topic_num_fk	FOREIGN KEY (topic_num)			REFERENCES topic(topic_num);

ALTER TABLE document_editor	ADD CONSTRAINT doc_id_fk	FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE document_editor	ADD CONSTRAINT editor_id_fk	FOREIGN KEY (editor_id)			REFERENCES editor(editor_id);
ALTER TABLE document_editor	ADD CONSTRAINT editor_role_fk	FOREIGN KEY (editor_role)		REFERENCES editor_role(editor_role);
ALTER TABLE document_maintainer	ADD CONSTRAINT doc_id_fk	FOREIGN KEY (doc_id)			REFERENCES document(doc_id);
ALTER TABLE document_maintainer	ADD CONSTRAINT maintainer_id_fk	FOREIGN KEY (maintainer_id)		REFERENCES maintainer(maintainer_id);
ALTER TABLE document_maintainer	ADD CONSTRAINT role_fk		FOREIGN KEY (role)			REFERENCES role(role);
ALTER TABLE maintainer_notes	ADD CONSTRAINT maintainer_id_fk	FOREIGN KEY (maintainer_id)		REFERENCES maintainer(maintainer_id);

