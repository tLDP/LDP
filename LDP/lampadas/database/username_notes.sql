CREATE TABLE username_notes
(
	user_id			INT4		NOT NULL,
	date_entered		TIMESTAMP	NOT NULL DEFAULT now(),
	notes			TEXT,
	creator_id		INT4		NOT NULL,

	PRIMARY KEY (user_id, date_entered)
);
