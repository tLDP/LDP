ALTER TABLE document		ADD CONSTRAINT class_id_fk		FOREIGN KEY (class_id)			REFERENCES class(class_id);
ALTER TABLE document		ADD CONSTRAINT format_id_fk		FOREIGN KEY (format_id)			REFERENCES format(format_id);
ALTER TABLE document		ADD CONSTRAINT dtd_fk			FOREIGN KEY (dtd)			REFERENCES dtd(dtd);
ALTER TABLE document		ADD CONSTRAINT pub_status_fk		FOREIGN KEY (pub_status)		REFERENCES pub_status(pub_status);
ALTER TABLE document		ADD CONSTRAINT review_status_fk		FOREIGN KEY (review_status)		REFERENCES review_status(review_status);
ALTER TABLE document		ADD CONSTRAINT tech_status_fk		FOREIGN KEY (tech_review_status)	REFERENCES review_status(review_status);
ALTER TABLE document		ADD CONSTRAINT license_fk		FOREIGN KEY (license)			REFERENCES license(license);
ALTER TABLE document		ADD CONSTRAINT language_fk		FOREIGN KEY (lang)			REFERENCES language(isocode);
