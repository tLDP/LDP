m4_define(insert,m4_dnl
[INSERT INTO log(log_id, level, username, message)
VALUES ($1, $2, '$3', '$4');])m4_dnl
