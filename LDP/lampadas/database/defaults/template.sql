DELETE FROM template;

INSERT INTO template (template_code, template) VALUES ('default',
'
<html>
  <head>
    <title>|title|</title>
  </head>
  <body>
    <table width=100%>
      <tr><td>|header|</td></tr>
      <tr><td>|body|</td></tr>
      <tr><td>|footer|</td></tr>
    </table>
  </body>
</html>
');

