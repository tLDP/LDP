<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="*|@*|comment()|processing-instruction()|text()">
    <xsl:copy>
      <xsl:apply-templates 
           select="*|@*|comment()|processing-instruction()|text()" />
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
