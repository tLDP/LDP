m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO news(news_id, pub_date)
VALUES ($1, '$2');])m4_dnl
