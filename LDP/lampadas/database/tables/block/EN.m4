insert([blkhead], [
<head>
    <title>|title|</title>
    <link rel="stylesheet" href="|uri.base|css/ldp.css" type="text/css">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>])

insert([blklogo], [
<table class="logo">
  <tr>
    <td valign="top">
      <a href="|uri.base|home|uri.lang_ext|">
      <img src="|uri.base|images/logos/ldp200x80.png" alt="LDP" height="80" width="200">
      </a>
    </td>
  </tr>
</table>])

insert([blkheader], [
<table class="header" width="100%">
  <tr>
    <td>
      <h1>|strproject|</h1>
      <h2>|title|</h2>
    </td>
  </tr>
</table> ])

insert([blkfooter], [
<table class="footer" width="100%">
  <tr>
    <td align="center">
      <a href="|uri.base|copyright|uri.lang_ext|">|strcopyright|</a> \\|
      <a href="|uri.base|privacy|uri.lang_ext|">|strprivacy|</a> \\|
      <a href="|uri.base|lampadas|uri.lang_ext|">|strabout_lamp|</a>
    </td>
  </tr>
</table>
<center>
  <a href="http://www.python.org"><img src="|uri.base|images/logos/PythonPowered.gif" alt="Python Powered!"></a>
  <a href="http://www.opensource.org"><img src="http://www.opensource.org/trademarks/osi-certified/web/osi-certified-90x75.png" height=75 width=90 alt="OSI Certified"></a>
  <a href="http://www.gnome.org"><img src="|uri.base|images/logos/gnome2.png" height="48" width="48" alt="Gnome"></a>
  <a href="http://www.tldp.org"><img src="|uri.base|images/logos/ldp200x80.png" width="200" height="80" alt="TLDP"></a>
  <br>|strrender_time|: |elapsed_time|
</center>])

insert([blknopermission], [
<table class="box" width="100%">
  <tr>
    <th>|strerror|</th>
  </tr>
  <tr>
    <td>|strnopermission|</td>
  </tr>
</table>])

insert([blknotfound], [
<table class="box" width="100%">
  <tr>
    <th>|strerror|</th>
  </tr>
  <tr>
    <td>|strnotfound|</td>
  </tr>
</table>])
