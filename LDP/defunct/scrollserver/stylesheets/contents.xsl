<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:include href="header.xsl"/>

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
  <h2>
  <xsl:value-of select="title"/>
  </h2>
  <xsl:apply-templates select="doc"/>
  <xsl:apply-templates select="sect[//doc]"/>
</xsl:template>

<xsl:template match="ScrollKeeperContentsList/sect/sect[//doc]">
  <h3>
  <xsl:value-of select="title"/>
  </h3>
  <xsl:apply-templates select="doc"/>
  <xsl:apply-templates select="sect[//doc]"/>
</xsl:template>

<xsl:template match="ScrollKeeperContentsList/sect/sect/sect[//doc]">
  <h4>
  <xsl:value-of select="title"/>
  </h4>
  <xsl:apply-templates select="doc"/>
  <xsl:apply-templates select="sect[//doc]"/>
</xsl:template>

<xsl:template match="sect//doc">
  <a href="docid?{@docid}">
  <xsl:value-of select="doctitle"/></a>
  <br></br>
</xsl:template>

<xsl:template match="/">
  <html>
  <head>
    <title>ScrollServer Contents List</title>
    <link rel="stylesheet" href="stylesheets/css/default.css" type="text/css"/>
  </head>
  <body>
    <xsl:call-template name="header"/>
    <h1>
    ScrollKeeper Contents List
    </h1>
    <xsl:apply-templates/>
    <p/>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
