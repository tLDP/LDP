CREATE TABLE log
(
	level			INT4		NOT NULL,
	username		CHAR(40),
	message			TEXT		NOT NULL,
	doc_id			INT4,
	created			TIMESTAMP	NOT NULL	DEFAULT now()
);

CREATE INDEX log_idx ON log (created);
CREATE INDEX log_username_idx ON log (username);
CREATE INDEX log_doc_id_idx ON log (doc_id);
CREATE INDEX log_level_idx ON log (level);

