ALTER TABLE username_notes	ADD CONSTRAINT user_id_fk		FOREIGN KEY (user_id)			REFERENCES username(user_id);
ALTER TABLE username_notes	ADD CONSTRAINT creator_id_fk		FOREIGN KEY (creator_id)		REFERENCES username(user_id);
