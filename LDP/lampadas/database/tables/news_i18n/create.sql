CREATE TABLE news_i18n
(
	news_id			INT4		NOT NULL	REFERENCES news(news_id),
	lang			CHAR(2)		NOT NULL	REFERENCES language(lang_code),
	news			TEXT		NOT NULL,
	headline		CHAR(120)	NOT NULL,
	version			CHAR(12)	NOT NULL DEFAULT '1.0',
	created			TIMESTAMP	NOT NULL DEFAULT now(),
	updated			TIMESTAMP	NOT NULL DEFAULT now(),

	PRIMARY KEY (news_id, lang)
);
