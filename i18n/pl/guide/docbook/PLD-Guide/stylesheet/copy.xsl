<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="*|@*|processing-instruction()|text()">
    <xsl:copy>
      <xsl:apply-templates 
           select="*|@*|comment()|processing-instruction()|text()" />
    </xsl:copy>
  </xsl:template>

  <xsl:template match="comment()">
    <xsl:if test="starts-with(normalize-space(.), 'web-hack ')">
      <xsl:apply-templates 
           select="document(concat('../', substring-after(normalize-space(.), 'web-hack ')))"
       />
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
