m4_define(insert,m4_dnl
[INSERT INTO log(level, username, message)
VALUES ($1, '$2', '$3');])m4_dnl
