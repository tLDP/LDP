<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/project-list">
    <xsl:apply-templates select="project" />
  </xsl:template>

  <xsl:output indent="yes" />

  <xsl:template match="project">
    <para>
    <table>
      <title><xsl:value-of select="name"/></title>
      <tgroup cols="2">
       <tbody>
        <row>
	  <entry><emphasis>Name:</emphasis></entry>
	  <entry><xsl:value-of select="name"/></entry>
	</row>
	<xsl:apply-templates select="maintainer"/>
        <row>
	  <entry><emphasis>Status:</emphasis></entry>
	  <entry><xsl:value-of select="status"/></entry>
	</row>
        <row>
	  <entry><emphasis>Location:</emphasis></entry>
	  <entry><filename><xsl:value-of select="location"/></filename></entry>
	</row>
        <row>
	  <entry><emphasis>Description:</emphasis></entry>
	  <entry><xsl:value-of select="description"/></entry>
	</row>
       </tbody>
      </tgroup>
    </table>
    </para>
  </xsl:template>

  <xsl:template match="maintainer">
    <xsl:variable name="email">
      <xsl:value-of 
         select="concat(substring-before(email,'@'), ' /at/ ', substring-after(email,'@'))"/>
    </xsl:variable>
    <row>
      <entry><emphasis>Maintainer:</emphasis></entry>
      <entry>
        <xsl:value-of select="name"/>
	&lt;<xsl:value-of select="$email"/>&gt;
      </entry>
    </row>
  </xsl:template>
</xsl:stylesheet>
