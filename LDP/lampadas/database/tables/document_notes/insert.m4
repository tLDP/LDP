m4_define(insert, [INSERT INTO document_note(note_id, doc_id, date_entered, creator, note)
VALUES ($1, $2, '$3', '$4', '$5');])m4_dnl
