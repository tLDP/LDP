m4_define(insert,
[INSERT INTO document_rev(rev_id, doc_id, version, pub_date, initials, notes)
VALUES ($1, $2, '$3', '$4', '$5', '$6');])m4_dnl
