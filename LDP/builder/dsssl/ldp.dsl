<!DOCTYPE style-sheet PUBLIC "-//James Clark//DTD DSSSL Style Sheet//EN" [
<!ENTITY % html "IGNORE">
<![%html;[
<!ENTITY % print "IGNORE">
<!ENTITY docbook.dsl SYSTEM "docbook.dsl" CDATA dsssl>
]]>
<!ENTITY % print "INCLUDE">
<![%print;[
<!ENTITY docbook.dsl SYSTEM "docbook.dsl" CDATA dsssl>
]]>
]>

<style-sheet>

<style-specification id="print" use="docbook">
<style-specification-body> 

;; ==============================
;; customize the print stylesheet
;; ==============================

</style-specification-body>
</style-specification>


<!--
;; ===================================================
;; customize the html stylesheet; borrowed from Cygnus
;; at http://sourceware.cygnus.com/ (cygnus-both.dsl)
;; ===================================================
-->

<style-specification id="html" use="docbook">
<style-specification-body> 

;; this is necessary because right now jadetex does not understand
;; symbolic entities, whereas things work well with numeric entities.
(declare-characteristic preserve-sdata?
  "UNREGISTERED::James Clark//Characteristic::preserve-sdata?"
  #f)

;; put the legal notice in a separate file
(define %generate-legalnotice-link%
  #t)

;; use graphics in admonitions, and have their path be "stylesheet-images"
;; NO: they do not yet look very good
(define %admon-graphics-path%
  "./stylesheet-images/")

(define %admon-graphics%
  #f)

(define %funcsynopsis-decoration%
  ;; make funcsynopsis look pretty
  #t)

(define %html-ext%
  ".html")

(define %generate-article-toc% 
  ;; Should a Table of Contents be produced for Articles?
  ;; If true, a Table of Contents will be generated for each 'Article'.
  #t)

(define %root-filename%
  ;; The filename of the root HTML document (e.g, "index").
  "index")

(define %generate-part-toc%
  #t)

(define %shade-verbatim%
  #t)

(define %use-id-as-filename%
  ;; Use ID attributes as name for component HTML files?
  #t)

(define %graphic-default-extension% 
  "gif")

(define (toc-depth nd)
  2)

</style-specification-body>
</style-specification>

<external-specification id="docbook" document="docbook.dsl">

</style-sheet>
