m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO audience(audience_code, audience_level, audience_description)
VALUES ('$1', $2, '$3');])m4_dnl
