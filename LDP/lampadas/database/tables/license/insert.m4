m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO license(license_code, free, sort_order)
VALUES ('$1', '$2', $3);])m4_dnl
