m4_define(insert,
[INSERT INTO sourcefile(filename, format_code, dtd_code, dtd_version, full_text)
VALUES ('$1', '$2', '$3', '$4', '$5');])m4_dnl
