m4_define(insert,
[INSERT INTO sourcefile_rev(rev_id, filename, version, pub_date, initials, notes)
VALUES ($1, '$2', '$3', '$4', '$5', '$6');])m4_dnl
