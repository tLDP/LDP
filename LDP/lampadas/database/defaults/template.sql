DELETE FROM template;

INSERT INTO template (template_code, template) VALUES ('default',
'
<table>
<tr><td>|header|</td></tr>
<tr><td>|body|</td></tr>
<tr><td>|footer|</td></tr>
</table>
');

