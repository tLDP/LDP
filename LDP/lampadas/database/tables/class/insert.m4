m4_changequote([, ])m4_dnl
m4_define(insert,m4_dnl
[INSERT INTO class(class_code, sort_order)
VALUES ('$1', $2);])m4_dnl
