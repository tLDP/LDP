m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO document(doc_id, lang, title, class_code, format_code,
dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status,
tickle_date, pub_date, ref_url, tech_review_status, maintained, license,
abstract, rating, sk_seriesid, replaced_by_id)
VALUES ($1, '$2', '$3', '$4', '$5',
'$6', '$7', '$8', '$9', '$10', '$11', '$12', '$13',
'$14', '$15', '$16', '$17', '$18', '$19',
'$20', $21, '$22', $23);])m4_dnl
