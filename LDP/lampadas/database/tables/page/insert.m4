m4_define(insert,
[INSERT INTO page(page_code, template_code, section_code, sort_order,
data,
only_dynamic, only_registered, only_admin, only_sysadmin)
VALUES ('$1', '$2', '$3', $4,
'$5',
'$6', '$7', '$8', '$9');])m4_dnl
