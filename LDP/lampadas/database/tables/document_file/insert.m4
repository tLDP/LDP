m4_define(insert,
[INSERT INTO document_file(doc_id, filename, top, format_code)
VALUES ($1, '$2', '$3', '$4');])m4_dnl
