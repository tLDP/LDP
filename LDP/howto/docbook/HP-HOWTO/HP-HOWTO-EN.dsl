<!DOCTYPE style-sheet PUBLIC "-//James Clark//DTD DSSSL Style Sheet//EN" [
<!-- Cas HTML -->
<!ENTITY html-ss
         PUBLIC "-//Norman Walsh//DOCUMENT DocBook HTML Stylesheet//EN"
         CDATA DSSSL>
<!-- Cas PS -->
<!ENTITY print-ss
		PUBLIC "-//Norman Walsh//DOCUMENT DocBook Print Stylesheet//EN" 
		CDATA DSSSL>
]>

<style-sheet>

<!-- Pour le HTML -->
<style-specification id="html" use="html-stylesheet">
<style-specification-body>

;; Courtoisement du projet de documentation FreeBSD

;; Use tables to build the navigation headers and footers?
(define %gentext-nav-use-tables% #t)

;; Default extension for HTML output files
(define %html-ext% ".html")

;; Name for the root HTML document
(define %root-filename% "index")

;; Should verbatim environments be shaded?
(define %shade-verbatim% #t)

;; Write a manifest? 
(define html-manifest #t)

;; Courtoisement de la part de S. Bortzmeyer
(element urlsgml
          (make sequence
            (make element
              gi: "A"
			  attributes: `(("HREF"
                             ,(data (current-node)))
              (data (current-node))))
			)
)
;; l'extension par défaut en mode HTML
(define %graphic-default-extension% "gif")

;; Custom headers

(define %html-header-tags%
  '(("META" ("HTTP-EQUIV" "Content-Type") ("CONTENT" "text/html; charset=iso-8859-1")) ("META" ("NAME" "Author") ("CONTENT" "Bruno Cornec")) ("META" ("NAME" "KeyWords") ("CONTENT" "Linux,HP,Medasys,HP-UX,Hewlett,Packard,France")))
	)
</style-specification-body>
</style-specification>

<!-- pour le PS -->
<style-specification id="print" use="print-stylesheet">
<style-specification-body>

;; Ne montre pas les liens
(define %show-ulinks% #f)

;; liens en bas de page ?
(define %footnote-ulinks% #t)





;; To make the following item work
(define tex-backend #t)
;; Make "bottom-of-page" footnotes?
(define bop-footnotes #f)

;; Allow justification
(define %default-quadding% 'justify)

;; Allow automatic hyphenation?
(define %hyphenation% #t)

;; urlsgml ne fait rien dans ce mode
(element urlsgml ($mono-seq$))

;; l'extension par défaut en mode print
(define %graphic-default-extension% "eps")

</style-specification-body>
</style-specification>

<external-specification id="html-stylesheet" document="html-ss">
<external-specification id="print-stylesheet" document="print-ss">

</style-sheet>
