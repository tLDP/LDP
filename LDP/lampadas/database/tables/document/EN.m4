insert(503, [Lampadas Developers Guide], 7, 6,
    [], [], [], [], [], [], [N], [U],
    [], [], [], [U], [t], [GFDL],
    [], 0, [EN], [])


m4_changequote([, ])m4_dnl
m4_define(insert, [INSERT INTO document(doc_id, title, class_id, format_id,
dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status,
tickle_date, pub_date, ref_url, tech_review_status, maintained, license,
abstract, rating, lang, sk_seriesid)
VALUES ($1, '$2', $3, $4,
'$5', '$6', '$7', '$8', '$9', '$10', '$11', '$11',
'$12', '$13', '$14', '$15', '$16', '$17',
'$18', $19, '$20', '$21');])m4_dnl
