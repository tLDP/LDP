<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:include href="header.xsl"/>

<xsl:template match="/">
  <html>
  <head>
    <title>ScrollServer Cache Reset</title>
    <link rel="stylesheet" href="stylesheets/css/default.css" type="text/css"/>
  </head>
  <body>

  <xsl:call-template name="header"/>

  <h1>ScrollServer Cache Reset</h1>

  <p>The ScrollServer document cache has been reset.
  </p>
  
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
