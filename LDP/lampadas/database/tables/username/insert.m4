m4_define(insert,
[INSERT INTO username(username, first_name, middle_name,
surname, email, admin, sysadmin, password, notes, stylesheet)
VALUES ('$1', '$2', '$3', '$4',
'$5', '$6', '$7', '$8', '$9', '$10');])m4_dnl
