DROP VIEW vw_active_authors;

CREATE VIEW vw_active_authors AS
SELECT DISTINCT
	dm.email
FROM	document_maintainer dm,
	document d
WHERE	dm.doc_id = d.doc_id
AND	d.pub_status = 'N'
AND	email <> ''
ORDER BY email;

