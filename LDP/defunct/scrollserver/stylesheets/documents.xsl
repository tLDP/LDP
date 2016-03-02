<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:include href="header.xsl"/>

<xsl:template match="text()">
<!--  <xsl:value-of select="."/> -->
</xsl:template>

<xsl:variable name="ucletters" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
<xsl:variable name="lcletters" select="'abcdefghijklmnopqrstuvwxyz'"/>

<xsl:template match="doc">
  <!--  don't display items with the same title more than once  -->
  <xsl:if test="preceding::doctitle!=doctitle">
    <a href="docid?{@docid}">
    <xsl:value-of select="doctitle"/></a>
    <br/>
  </xsl:if>
</xsl:template>

<xsl:template match="/">
  <html>
  <head>
    <title>ScrollServer Document List</title>  
    <link rel="stylesheet" href="stylesheets/css/default.css" type="text/css"/>
  </head>
  <body>
    <xsl:call-template name="header"/>
    <h1>ScrollKeeper Document List</h1>
    <xsl:apply-templates select="//doc">
      <xsl:sort select="translate(doctitle, $lcletters, $ucletters)"/>
    </xsl:apply-templates>
    <p/>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
