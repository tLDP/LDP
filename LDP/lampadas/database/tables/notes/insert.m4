m4_define(insert, [INSERT INTO notes(note_id, doc_id, date_entered, creator, notes)
VALUES ($1, $2, '$3', '$4', '$5');])m4_dnl
