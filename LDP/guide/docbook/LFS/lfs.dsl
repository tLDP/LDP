<!DOCTYPE style-sheet PUBLIC "-//James Clark//DTD DSSSL Style Sheet//EN" [
<!ENTITY docbook.dsl SYSTEM "docbook.dsl" CDATA dsssl>
]>

<style-sheet>

<style-specification use="docbook">
<style-specification-body>

(define %generate-legalnotice-link%
;; put the legal notice in a separate file
#t)

(define ($legalnotice-link-file$ legalnotice)
;; filename of the legalnotice file
(string-append "legalnotice"%html-ext%))

(define %html-ext%
;; html extenstion
".html")

(define %root-filename%
;; index file of the book
"index")

(define %use-id-as-filename%
;; filenames same as id attribute in title tags
#t)

(define %body-attr%
;; html body settings
(list
(list "BGCOLOR" "#FFFFFF")
(list "TEXT" "#000000")
(list "LINK" "#0000FF")
(list "VLINK" "#840084")
(list "ALINK" "#006000")))

(define (chunk-skip-first-element-list)
;; forces the Table of Contents on separate page
'())

(define (list-element-list)
;; fixes bug in Table of Contents generation
'())

(define %shade-verbatim%
;; verbatim sections will be shaded if t(rue)
#t)

;;(define %section-autolabel%
;; For enumerated sections (1.1, 1.1.1, 1.2, etc.)
;;#t)

(element emphasis
;; make role=strong equate to bold for emphasis tag
(if (equal? (attribute-string "role") "strong")
(make element gi: "STRONG" (process-children))
(make element gi: "EM" (process-children))))


</style-specification-body>
</style-specification>

<external-specification id="docbook" document="docbook.dsl">

</style-sheet>

