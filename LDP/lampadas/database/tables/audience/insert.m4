m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO audience(audience_code, sort_order, audience_name, audience_desc)
VALUES ('$1', $2, '$3', '$4');])m4_dnl
