m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO audience(audience_code, sort_order)
VALUES ('$1', $2);])m4_dnl
