DROP TABLE topic_i18n;

CREATE TABLE topic_i18n
(
	topic_num		INT4		NOT NULL,
	lang			CHAR(2)		NOT NULL,
	topic_name		TEXT		NOT NULL,
	topic_description	TEXT,

	PRIMARY KEY (topic_num, lang)
);
