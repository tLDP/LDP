CREATE TABLE block
(
	block_code		CHAR(20)	NOT NULL,
	block			TEXT,
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (block_code)
);
