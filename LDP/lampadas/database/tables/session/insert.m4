m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO session(session_id, username)
VALUES ('$1', '$2');])m4_dnl
