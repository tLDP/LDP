<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:include href="header.xsl"/>

<xsl:template match="/">
  <html>
  <head>
    <title>ScrollServer</title>
    <link rel="stylesheet" href="default.css" type="text/css"/>
  </head>
  <body>

  <xsl:call-template name="header"/>

  <h1>Welcome to ScrollServer</h1>

  <p>You can use ScrollServer to browse and search help files that are installed
    on your computer as well as online ScrollServer databases.
  </p>

  <p>ScrollServer is a young project that is still in early development, so many
    features are not yet implemented. You should find it usable but incomplete.
  </p>
  
  <p>Please report bugs and request features by writing to the author at
    <a href="mailto:david@lupercalia.net">david@lupercalia.net</a>.
  </p>
  
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
