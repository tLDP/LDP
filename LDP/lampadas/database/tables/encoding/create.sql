CREATE TABLE encoding
(
	encoding		CHAR(12)	NOT NULL,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (encoding)
);
