m4_define(insert, [INSERT INTO document_user(doc_id, username, role_code, email, active)
VALUES ($1, '$2', '$3', '$4', '$5');])m4_dnl
