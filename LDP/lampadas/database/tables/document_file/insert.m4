m4_define(insert,
[INSERT INTO document_file(doc_id, filename, top)
VALUES ($1, '$2', '$3');])m4_dnl
