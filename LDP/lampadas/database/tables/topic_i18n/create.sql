CREATE TABLE topic_i18n
(
	topic_num		INT4		NOT NULL
				REFERENCES topic(topic_num),
	lang			CHAR(2)		NOT NULL
				REFERENCES language(isocode),
	topic_name		TEXT		NOT NULL,
	topic_description	TEXT,

	PRIMARY KEY (topic_num, lang)
);
