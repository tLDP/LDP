insert(default,
[
	<html>
	  <head>
	    <title>|title|</title>
	    <base href="|base|">
	    <link rel="stylesheet" href="css/|stylesheet|.css" type="text/css">
	  </head>
	  <body>
	    <table class="layout" style="width:100%">
	      <tr><td colspan=2>|header|</td></tr>
	      <tr>
            <td width="200" valign="top">
              <table class="margin"><tr><td>
                |tabmenus|
              </td></tr></table>
            </td>
            <td valign="top" class="body">
              <table class="body"><tr><td>
                |body|
              </td></tr></table>
            </td>
	      </tr>
	    <tr><td colspan=2>|footer|</td></tr>
	    </table>
	  </body>
	</html>
])
