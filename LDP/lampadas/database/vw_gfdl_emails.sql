DROP VIEW vw_gfdl_emails;

CREATE VIEW vw_gfdl_emails AS
SELECT DISTINCT
	m.email
FROM 	maintainer m,
	document_maintainer dm,
	document d
WHERE	m.maintainer_id = dm.maintainer_id
AND	dm.doc_id = d.doc_id
AND	d.license <> 'GFDL'
AND 	d.license <> 'GPL'
AND	d.license <> 'OPL'
AND	m.email <> ''
ORDER BY email;

