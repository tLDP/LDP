CREATE TABLE deleted
(
	table_name		CHAR(40)	NOT NULL,
	identifier		TEXT		NOT NULL,
	deleted			TIMESTAMP	NOT NULL DEFAULT now()
);

CREATE INDEX deleted_idx ON deleted (deleted);
