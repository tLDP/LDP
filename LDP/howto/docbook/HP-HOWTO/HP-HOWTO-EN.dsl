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

;; Are sections enumerated?
(define %section-autolabel% #t)

;; Use graphics in admonitions?
(define %admon-graphics% #t)

;; Path to admonition graphics
(define %admon-graphics-path% "images/")

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
(define %graphic-default-extension% "png")

(define %generate-part-toc%
  #t)

;; Use ID attributes as name for component HTML files? (Greg Ferguson)
(define %use-id-as-filename% #t)

;; Custom headers

(define %html-header-tags%
  '(("META" ("HTTP-EQUIV" "Content-Type") ("CONTENT" "text/html; charset=iso-8859-1")) ("META" ("NAME" "Author") ("CONTENT" "Bruno Cornec")) ("META" ("NAME" "KeyWords") ("CONTENT" "Linux,HP,Medasys,HP-UX,Hewlett,Packard,France")))
	)

;; Courtoisement de Mark Johnson
;; Turn on fast-forward link generation 
(define %gentext-nav-use-ff% #t)

;; ---------------------
;;    Navigation Icons
;; ---------------------
;;
;; Redefine links as graphic icons instead of text
;;
;; (Overrides definitions in common/dbl1en.dsl)
;;
(define (gentext-en-nav-prev prev)
    (make empty-element gi: "IMG"
           attributes: '(("SRC" "../images/prev.png")
   ("BORDER" "0")
                        ("ALT" "Prev"))))

(define (gentext-en-nav-prev-sibling prevsib)
    (make empty-element gi: "IMG"
           attributes: '(("SRC" "../images/fast-bak.png")
   ("BORDER" "0")
                        ("ALT" "Fast Backward"))))

(define (gentext-en-nav-next-sibling nextsib)
    (make empty-element gi: "IMG"
           attributes: '(("SRC" "../images/fast-for.png")
   ("BORDER" "0")
                        ("ALT" "Fast Forward"))))

(define (gentext-en-nav-next next)
    (make empty-element gi: "IMG"
           attributes: '(("SRC" "../images/next.png")
   ("BORDER" "0")
                        ("ALT" "Next"))))

(define (gentext-en-nav-up up)
    (make empty-element gi: "IMG"
           attributes: '(("SRC" "../images/up.png")
   ("BORDER" "0")
                        ("ALT" "Up"))))

(define (gentext-en-nav-home home)
    (make empty-element gi: "IMG"
           attributes: '(("SRC" "../images/home.png")
   ("BORDER" "0")
                        ("ALT" "Home"))))

;;
;;
;;=================================================================
;;         End of navigation icons section
;;=================================================================


;;=================================================================
;;    NAVIGATION HEADER TABLES
;;=================================================================
;;
;;
;; Rearrange navigation header to put bigger jumps at outside edge
;;
;; (Overrides stuff defined in html/dbnavig.dsl)
;;
;;
;;=================================================================
;;=================================================================
;;
;;

(define (default-header-nav-tbl-ff elemnode prev next prevsib nextsib)
  (let* ((r1? (nav-banner? elemnode))
  (r1-sosofo (make element gi: "TR"
     (make element gi: "TH"
    attributes: (list
          (list "COLSPAN" "5")
          (list "ALIGN" "center")
          (list "VALIGN" "bottom"))
    (nav-banner elemnode))))
  (r2? (or (not (node-list-empty? prev))
    (not (node-list-empty? next))
    (not (node-list-empty? prevsib))
    (not (node-list-empty? nextsib))
    (nav-context? elemnode)))
  (r2-sosofo (make element gi: "TR"

;; constructs Fast-Backward link

     (make element gi: "TD"
    attributes: (list
          (list "WIDTH" "10%")
          (list "ALIGN" "left")
          (list "VALIGN" "top"))
    (if (node-list-empty? prevsib)
        (make entity-ref name: "nbsp")
        (make element gi: "A"
       attributes: (list
             (list "HREF"
            (href-to
             prevsib)))
       (gentext-nav-prev-sibling prevsib))))

;; constructs Previous link
     (make element gi: "TD"
    attributes: (list
          (list "WIDTH" "10%")
          (list "ALIGN" "left")
          (list "VALIGN" "top"))
    (if (node-list-empty? prev)
        (make entity-ref name: "nbsp")
        (make element gi: "A"
       attributes: (list
             (list "HREF"
            (href-to
             prev)))
       (gentext-nav-prev prev))))

;; center part: navigation context, title, etc.

     (make element gi: "TD"
    attributes: (list
          (list "WIDTH" "60%")
          (list "ALIGN" "center")
          (list "VALIGN" "bottom"))
    (nav-context elemnode))
;; constructs Next link
     (make element gi: "TD"
    attributes: (list
          (list "WIDTH" "10%")
          (list "ALIGN" "right")
          (list "VALIGN" "top"))
    (if (node-list-empty? next)
        (make entity-ref name: "nbsp")
        (make element gi: "A"
       attributes: (list
             (list "HREF"
            (href-to
             next)))
       (gentext-nav-next next))))

;; constructs Fast-Forward link

     (make element gi: "TD"
    attributes: (list
          (list "WIDTH" "10%")
          (list "ALIGN" "right")
          (list "VALIGN" "top"))
    (if (node-list-empty? nextsib)
        (make entity-ref name: "nbsp")
        (make element gi: "A"
       attributes: (list
             (list "HREF"
            (href-to
             nextsib)))
       (gentext-nav-next-sibling nextsib))))
                                                       )))
    (if (or r1? r2?)
 (make element gi: "DIV"
       attributes: '(("CLASS" "NAVHEADER"))
   (make element gi: "TABLE"
  attributes: (list
        (list "WIDTH" %gentext-nav-tblwidth%)
        (list "BORDER" "0")
        (list "CELLPADDING" "0")
        (list "CELLSPACING" "0"))
  (if r1? r1-sosofo (empty-sosofo))
  (if r2? r2-sosofo (empty-sosofo)))
   (make empty-element gi: "HR"
  attributes: (list
        (list "ALIGN" "LEFT")
        (list "WIDTH" %gentext-nav-tblwidth%))))
 (empty-sosofo))))

;;
;;
;;=================================================================


</style-specification-body>
</style-specification>

<!-- pour le PS -->
<style-specification id="print" use="print-stylesheet">
<style-specification-body>

;; Ne montre pas les liens
(define %show-ulinks% #f)

;; Are sections enumerated?
(define %section-autolabel% #t)

;; Use graphics in admonitions?
(define %admon-graphics% #t)

;; Path to admonition graphics
(define %admon-graphics-path% "images/")

(define ($admon-graphic$ #!optional (nd (current-node)))
      (cond ((equal? (gi nd) (normalize "tip"))
             (string-append %admon-graphics-path% "tip.eps"))
            ((equal? (gi nd) (normalize "note"))
             (string-append %admon-graphics-path% "note.eps"))
            ((equal? (gi nd) (normalize "important"))
             (string-append %admon-graphics-path% "important.eps"))
            ((equal? (gi nd) (normalize "caution"))
             (string-append %admon-graphics-path% "caution.eps"))
            ((equal? (gi nd) (normalize "warning"))
             (string-append %admon-graphics-path% "warning.eps"))
            (else (error (string-append (gi nd) " is not an admonition.")))))





;; liens en bas de page ?
(define %footnote-ulinks% #t)

;; Make "bottom-of-page" footnotes?
;;(define bop-footnotes #t)

;; Allow justification
(define %default-quadding% 'justify)

;; Allow automatic hyphenation?
(define %hyphenation% #t)

;; urlsgml ne fait rien dans ce mode
(element urlsgml ($mono-seq$))

;; l'extension par défaut en mode print
(define %graphic-default-extension% "eps")

;; Courtoisement de Norman Walsh 
(define (book-titlepage-recto-elements)
  (list (normalize "title")
        (normalize "subtitle")
        (normalize "graphic")
        (normalize "mediaobject")
        (normalize "corpauthor")
        (normalize "authorgroup")
        (normalize "author")
        (normalize "editor")
        ;;(normalize "copyright")
        (normalize "printhistory") ;; add this...
        ;;(normalize "revhistory")
        ;;(normalize "abstract")
		;;(normalize "releaseinfo")
		(normalize "pubdate")
        ;;(normalize "legalnotice")
	))                   

</style-specification-body>
</style-specification>

<!-- Pour le TXT -->
<style-specification id="txt" use="html">
<style-specification-body>

;; Un seul morceau
(define nochunks #t)

;; pas de manifest
(define %html-manifest% #f)

</style-specification-body>
</style-specification>

<external-specification id="html-stylesheet" document="html-ss">
<external-specification id="print-stylesheet" document="print-ss">

</style-sheet>
