m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO pub_status(pub_status, sort_order)
VALUES ('$1', $2);])m4_dnl
