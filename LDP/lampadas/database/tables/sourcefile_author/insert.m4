m4_define(insert,
[INSERT INTO sourcefile_author(filename, firstname, othername, surname, email)
VALUES ('$1', '$2', '$3', '$4', '$5');])m4_dnl
