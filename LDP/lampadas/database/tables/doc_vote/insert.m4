m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO doc_vote(doc_id, user_id, vote)
VALUES ($1, $2, $3);])m4_dnl
