m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO page(page_code, template_code, section_code, sort_order)
VALUES ('$1', '$2', '$3', $4);])m4_dnl
