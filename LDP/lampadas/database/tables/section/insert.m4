m4_define(insert,m4_dnl
[INSERT INTO section(section_code, sort_order, only_registered, only_admin, only_sysadmin)
VALUES ('$1', $2, '$3', '$4', '$5');])m4_dnl
