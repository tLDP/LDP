m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO page(page_code, section_code, template_code)
VALUES ('$1', '$2', '$3');])m4_dnl
