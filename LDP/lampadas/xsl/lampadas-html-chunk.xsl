<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version='1.0'
                xmlns="http://www.w3.org/TR/xhtml1/transitional"
                exclude-result-prefixes="#default">

<!-- $Id$ -->

<!-- This stylesheet is based on the ldp-html-chunk.xsl stylesheet
     by Dan York -->

<!-- This stylesheet calls Norman Walsh's 'docbook.xsl' stylesheet
     and therefore generates MULTIPLE HTML FILES as output. -->

<!-- Note the the *order* of the import statements below is important and
     should not be changed. -->

<!-- Change this to the path to where you have installed Norman
     Walsh's XSL stylesheets -->
<xsl:import href="/usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/chunk.xsl"/>

<!-- Imports the common LDP customization layer. -->
<xsl:import href="lampadas-html-common.xsl"/>

<!-- If there was some reason to override 'lampadas-html-common.xsl' or to 
     perform any other customizations that affect *only* the generation
     of multiple HTML files, those templates or parameters could be
     entered here. -->

</xsl:stylesheet>
