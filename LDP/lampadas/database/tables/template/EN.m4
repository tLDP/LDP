insert(default,
[
	<html>
	  <head>
	    <title>|title|</title>
	    <base href="|base|">
	    <link rel="stylesheet" href="css/|stylesheet|.css" type="text/css">
	  </head>
	  <body>
	    <table class="layout">
	      <tr>
            <td>
              |header|
            </td>
	      </tr>
        </table>
	    <table class="layout">
	      <tr>
            <td class="sidebar">
              |tabmenus|
              |tabtopics|
              |tabtypes|
              |tablanguages|
            </td>
            <td class="body">
              |body|
            </td>
	      </tr>
        </table>
	    <table class="layout">
	      <tr>
            <td>
              |footer|
            </td>
	      </tr>
        </table>
	  </body>
	</html>
])

insert(index,
[
	<html>
	  <head>
	    <title>|title|</title>
	    <base href="|base|">
	    <link rel="stylesheet" href="css/|stylesheet|.css" type="text/css">
	  </head>
	  <body>
	    <table class="layout">
	      <tr>
            <td>
              |header|
            </td>
	      </tr>
        </table>
	    <table class="layout">
	      <tr>
            <td class="sidebar">
              |tabmenus|
              |tabtopics|
              |tabtypes|
              |tablanguages|
            </td>
            <td class="body">
              |body|
            </td>
            <td class="sidebar">
              |tablogin|
              |tabsessions|
            </td>
	      </tr>
        </table>
	    <table class="layout">
	      <tr>
            <td>
              |footer|
            </td>
	      </tr>
        </table>
	  </body>
	</html>
])
