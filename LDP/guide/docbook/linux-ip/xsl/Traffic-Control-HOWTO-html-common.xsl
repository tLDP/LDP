<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version='1.0'
                xmlns="http://www.w3.org/TR/xhtml1/transitional"
                exclude-result-prefixes="#default"
                >


<xsl:param name="html.stylesheet" select="'Traffic-Control-HOWTO.css'"/>

<!-- experimental -->

<xsl:param name="xref.with.number.and.title" select="1"/>
<xsl:param name="footer.rule" select="1"/>
<xsl:param name="header.rule" select="1"/>
<xsl:param name="callout.graphics.number.limit" select="20"/>


<!--
  Tried chunk.tocs.and.lots, and got a main page with revision history
  and abstract.  Not quite what I had hoped.

  <xsl:param name="chunk.tocs.and.lots" select="1"/>

  Appears to be used by the LDP stylesheets, on which this is based

  <xsl:param name="chunk.first.sections" select="1"/>

  Not much happened with this.  Hmph.

  <xsl:param name="xref.properties" select="'local'"/>

  Attempted, 2003-04-18, looks terrible; hard to navigate.

  <xsl:param name="generate.toc">
  book      toc
  part      toc,title
  appendix  toc,title,example
  section   toc,title
  </xsl:param>

  -->

<xsl:template match="ulink" name="ulink">
  <xsl:variable name="link">
    <a class="nonlocal">
      <xsl:if test="@id">
        <xsl:attribute name="name">
          <xsl:value-of select="@id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:attribute name="href"><xsl:value-of select="@url"/></xsl:attribute>
      <xsl:if test="$ulink.target != ''">
        <xsl:attribute name="target">
          <xsl:value-of select="$ulink.target"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:choose>
        <xsl:when test="count(child::node())=0">
          <xsl:value-of select="@url"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates/>
        </xsl:otherwise>
      </xsl:choose>
    </a>
  </xsl:variable>

      <xsl:copy-of select="$link"/>

  <!--
      commented out because of problems with error messages from
      xsltproc when trying to locate function "suwl"
  <xsl:choose>
    <xsl:when test="function-available('suwl:unwrapLinks')">
      <xsl:copy-of select="suwl:unwrapLinks($link)"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:copy-of select="$link"/>
    </xsl:otherwise>
  </xsl:choose>
    -->

</xsl:template>

<!-- this stylesheet should override Norm Walsh's base stylesheets
     and the LDP stylesheets to make it clear what links are local
     and what links are non-local. -->


</xsl:stylesheet>
