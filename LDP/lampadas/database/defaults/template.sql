DELETE FROM template;

INSERT INTO template (template_code, template) VALUES ('default',
'
<html>
  <head>
    <title>|title|</title>
  </head>
  <body>
    <table width=100%>
      <tr><td colspan=2>|header|</td></tr>
      <tr>
        <td width="200">|boxmainmenu|</td>
        <td>|body|</td>
      </tr>
      <tr><td colspan=2>|footer|</td></tr>
    </table>
  </body>
</html>
');

