m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO subtopic(subtopic_code, subtopic_num, topic_code)
VALUES ('$1', $2, '$3');])m4_dnl
