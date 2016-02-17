<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version='1.0'
                xmlns="http://www.w3.org/TR/xhtml1/transitional"
                exclude-result-prefixes="#default">

<!-- $Id$  -->

<!-- This stylesheet will eventually include print customizations
     from LDP.DSL.  At the current time, it has not been developed.-->

<!-- Change this to the path to where you have installed Norman
     Walsh's XSL stylesheets.  -->
<xsl:import href="http://docbook.sourceforge.net/release/xsl/current/fo/docbook.xsl"/>

<!-- Number all sections in the style of 'CH.S1.S2 Section Title' where
     CH is the chapter number,  S1 is the section number and S2 is the
     sub-section number.  The lables are not limited to any particular
     depth and can go as far as there are sections. -->
<xsl:param name="section.autolabel" select="1"></xsl:param>
<xsl:param name="section.label.includes.component.label" select="0"></xsl:param>

<!-- Turn off the default 'full justify' and go with 'left justify'
     instead.  This avoids the large gaps that can sometimes appear
     between words in fully-justified documents.  -->
<xsl:param name="alignment">start</xsl:param>

<!-- Shade Verbatim Sections such as programlisting and screen -->
<xsl:param name="shade.verbatim" select="1"/>

<!-- Create bookmarks in .PDF files -->
<xsl:param name="fop.extensions" select="0"/>

<!-- Use fop1 extensions, per 
     https://lists.oasis-open.org/archives/docbook-apps/201110/msg00080.html
  -->
<xsl:param name="fop1.extensions" select="1"/>


</xsl:stylesheet>
