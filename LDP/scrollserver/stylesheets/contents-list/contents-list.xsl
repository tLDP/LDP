<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:template match="text()">
<!--  <xsl:value-of select="."/> -->
</xsl:template>

<xsl:template match="ScrollKeeperContentsList">
  <h1>
  <xsl:value-of select="title"/>
  </h1>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="ScrollKeeperContentsList/sect[//doc]">
  <h1>
  <xsl:value-of select="title"/>
  </h1>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="ScrollKeeperContentsList/sect/sect[//doc]">
  <h2>
  <xsl:value-of select="title"/>
  </h2>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="doc">
  <a href="docid?{@docid}">
  <xsl:value-of select="doctitle"/></a>
  <br></br>
</xsl:template>

<xsl:template match="/">
  <html>
  <head>
    <title>ScrollServer</title>  
  </head>
  <body>
    <p>
      <a href="/index.html">Index</a>
    </p>
    <xsl:apply-templates/>
  </body>
  </html>
</xsl:template>

<!-- ==================================================================== -->

</xsl:stylesheet>
