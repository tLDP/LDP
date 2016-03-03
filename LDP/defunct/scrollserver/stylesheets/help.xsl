<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:include href="header.xsl"/>

<xsl:template match="/">
  <html>
  <head>
    <title>ScrollServer Help</title>
    <link rel="stylesheet" href="stylesheets/css/default.css" type="text/css"/>
  </head>
  <body>

  <xsl:call-template name="header"/>

  <h1>ScrollServer Help</h1>

  <h2>Navigation Bar</h2>

  <p>
  Click items on the navigation bar that appears on the top of each page
  to navigate the documentation.
  The meaning of each item on the navigation bar is listed below.
  </p>
  
  <dl>
  <dt>Home</dt>
  <dd>Return to the ScrollServer Home Page.</dd>
  <dt>Contents</dt>
  <dd>Display the Table of Contents.</dd>
  <dt>Documents</dt>
  <dd>Display an alphabetical list of all documents.</dd>
  <dt>Controls</dt>
  <dd>Control the way ScrollServer works. You can reset ScrollServer's internal
  document cache.</dd>
  <dt>Help</dt>
  <dd>Display this page.</dd>
  </dl>

  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
