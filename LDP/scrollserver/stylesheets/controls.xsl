<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:include href="header.xsl"/>

<xsl:template match="/">
  <html>
  <head>
    <title>ScrollServer Controls</title>
    <link rel="stylesheet" href="stylesheets/css/default.css" type="text/css"/>
  </head>
  <body>

  <xsl:call-template name="header"/>

  <h1>ScrollServer Controls</h1>

  <p>
  From this page you can control the operation of ScrollServer.
  </p>
  
  <p>
  <a href="reset.html">Reset the Cache</a>
  </p>
  
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
