m4_define(insert,
[INSERT INTO document_file(doc_id, filename, top, format_code, dtd_code, dtd_version)
VALUES ($1, '$2', '$3', '$4', '$5', '$6');])m4_dnl
