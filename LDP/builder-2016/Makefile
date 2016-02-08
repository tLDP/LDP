# -- Makefile for handling TLDP documentation
#
#

default: all

DESTDIR    := output
NODESTDIR  := $(shell stat 2>/dev/null -t $(DESTDIR))
ifeq ($(NODESTDIR),)
  $(error ENOENT (2): $(DESTDIR); please create or specify alternate DESTDIR directory)
endif

WORKING    := working
NOWORKING  := $(shell stat 2>/dev/null -t $(WORKING))
ifeq ($(NOWORKING),)
  $(error ENOENT (2): $(WORKING); please create or specify alternate WORKING directory)
endif

ifeq ($(OBJ),)
  $(error OBJ not specified, please supply a DocBook SGML source file)
endif

FLAVOR=$(shell awk -F= '/^ID=/{print $$2}' /etc/os-release)
ifeq ($(FLAVOR),ubuntu)
  # -- Ubuntu:
  # -- for DocBook SGML (DSSSL) processing
  LDPDSL     := /usr/share/sgml/docbook/stylesheet/dsssl/ldp/ldp.dsl
  DBDSL      := /usr/share/sgml/docbook/stylesheet/dsssl/modular/html/docbook.dsl
  COLLATE    := /usr/bin/collateindex.pl
  # -- for DocBook XML (XSLT layer) processing
  XSLCHUNK   := /usr/share/xml/docbook/stylesheet/ldp/html/tldp-sections.xsl
  XSLSINGLE  := /usr/share/xml/docbook/stylesheet/ldp/html/tldp-one-page.xsl
  XSLPRINT   := /usr/share/xml/docbook/stylesheet/ldp/fo/tldp-print.xsl
else ifeq ($(FLAVOR),opensuse)
  # -- OpenSUSE-13.2
  # -- for DocBook SGML (DSSSL) processing
  DBDSL      := /usr/share/sgml/docbook/dsssl-stylesheets-1.79/html/docbook.dsl
  COLLATE    := /usr/share/sgml/docbook/dsssl-stylesheets-1.79/bin/collateindex.pl
  LDPDSL     := /home/mabrown/vcs/LDP/LDP/builder/dsssl/ldp.dsl
  # -- for DocBook XML (XSLT layer) processing
  XSLCHUNK   := /home/mabrown/vcs/LDP/LDP/builder/xsl/ldp-html-chunk.xsl
  XSLSINGLE  := /home/mabrown/vcs/LDP/LDP/builder/xsl/ldp-html.xsl
  XSLPRINT   := /home/mabrown/vcs/LDP/LDP/builder/xsl/ldp-print.xsl
else
  $(error Sorry, unknown/untested flavor of Linux, $(FLAVOR))
endif

# -- standard definitions and other little tools
#
XML_CATALOG_FILES := /etc/xml/catalog
PERL              := $(shell which perl 2>/dev/null)
VERBOSE           :=

OBJDIR            := $(dir $(OBJ))
OBJFORMAT         := $(lastword $(subst ., ,$(suffix $(OBJ))))
OBJFILE           := $(notdir $(OBJ))
OBJSTEM           := $(OBJFILE:.$(OBJFORMAT)=)
OBJINDEX          := $(abspath $(OBJDIR)/index.sgml)

ifeq ($(OBJFORMAT),sgml)
  LINUXDOC := $(shell head -n 5 "$(OBJ)" | tr A-Z a-z | awk '/doctype linuxdoc system/{ print $$2}')
  ifeq ($(LINUXDOC),linuxdoc)
    OBJFORMAT = linuxdoc
  endif
endif

OUTDIR      = $(abspath $(abspath $(WORKING))/$(OBJSTEM))

FO          = $(abspath $(OUTDIR)/$(OBJSTEM).fo)
PDF         = $(abspath $(OUTDIR)/$(OBJSTEM).pdf)
HTML        = $(abspath $(OUTDIR)/$(OBJSTEM).html)
HTMLS       = $(abspath $(OUTDIR)/$(OBJSTEM)-single.html)
TEXT        = $(abspath $(OUTDIR)/$(OBJSTEM).txt)


# - - - - - - - - - - - - - - - - - - - - - - -
# generic targets
# - - - - - - - - - - - - - - - - - - - - - - -

all: announce clear_$(OUTDIR) $(OBJFORMAT)-all
	rsync $(VERBOSE) --archive --delay-updates --delete-after --partial $(OUTDIR)/ $(DESTDIR)/$(OBJSTEM)/

clear_$(OUTDIR):
	(test ! -d $(OUTDIR) || ( cd $(dir $(OUTDIR)) && rm -rf $(VERBOSE) -- $(notdir $(OUTDIR))))

$(OUTDIR): $(WORKING)
	mkdir $(OUTDIR)

$(OUTDIR)/images $(OUTDIR)/resources: $(OUTDIR)
	(cd $(OBJDIR) && test ! -d $(notdir $@) || rsync -aL $(VERBOSE) ./$(notdir $@) $(OUTDIR))

.PHONY: announce
announce:
	$(info Detected $(OBJ) file as $(OBJFORMAT).)

# - - - - - - - - - - - - - - - - - - - - - - -
# specific handling for DocBook SGML documents
# - - - - - - - - - - - - - - - - - - - - - - -

.PHONY: sgml-all
sgml-all: sgml-$(OBJINDEX) sgml-$(HTMLS) sgml-$(TEXT) sgml-$(PDF) sgml-$(HTML)
	rm -f -- "$(OBJINDEX)"

.PHONY: sgml-$(OBJINDEX)
sgml-$(OBJINDEX): $(OUTDIR)/images $(OUTDIR)/resources
	(cd $(OUTDIR) \
	  && $(PERL) $(COLLATE) -N -o "$(OBJINDEX)" \
	  && openjade -t sgml -V html-index -d "$(DBDSL)" "$(OBJ)" \
	  && $(PERL) $(COLLATE) -g -t Index -i doc-index -o "$(notdir $(OBJINDEX))" HTML.index "$(OBJ)" \
          && mv -f $(VERBOSE) -- $(notdir $(OBJINDEX)) $(dir $(OBJINDEX)) \
	  && find . -mindepth 1 -maxdepth 1 -type f -print0 | xargs --null --no-run-if-empty -- rm -f --)

.PHONY: sgml-$(HTMLS)
sgml-$(HTMLS): $(OUTDIR)/resources $(OUTDIR)/images $(INDEX) 
	# -- note the mv -vu $(notdir $(HTML)) $(notdir $(HTMLS))
	#    the docbook2html processor will create a single-page
	#    HTML file called $(OBJSTEM).html.  We want to name it
	#    $(OBJSTEM)-single.html, so that, later, $(OBJSTEM).html
	#    can be the main output for chunked HTML
	#
	(cd $(OUTDIR) \
	  && jw -f docbook -b html \
	        --dsl "$(LDPDSL)#html" \
	        -V nochunks \
	        -V '%callout-graphics-path%=images/callouts/' \
	        -V '%stock-graphics-extension%=.png' \
	        -V '%stylsheet-type%=freddie.css' \
	      --output . \
	      $(OBJ) \
	  && mv --update $(VERBOSE) -- $(notdir $(HTML)) $(notdir $(HTMLS)))

.PHONY: sgml-$(TEXT)
sgml-$(TEXT): sgml-$(HTMLS)
	(cd $(OUTDIR) && html2text -style pretty -nobs $(notdir $(HTMLS)) > $(notdir $@))

.PHONY: sgml-$(PDF)
sgml-$(PDF): $(OUTDIR)
	( cd $(OUTDIR) \
          && jw -f docbook -b pdf --output . $(OBJ) \
	  || dblatex -F sgml -t pdf -o sgml-$(PDF) $(OBJ))

.PHONY: sgml-$(HTML)
sgml-$(HTML): $(OUTDIR)
	# -- the jade DocBook processing toolchain produces an HTML output
	#    file called index.html in the chunked output; therefore, we want
	#    to create a link from Some-Name.html to index.html; if TLDP
	#    wishes to do something else with index.html, this is the place
	#    to change it (for SGML DocBook inputs, anyway).
	#
	( cd $(OUTDIR) \
	  && jw -f docbook -b html  \
	      --dsl "$(LDPDSL)#html" \
	      -V '%admon-graphics-path%=images/' \
	      -V '%callout-graphics-path%=images/callouts/' \
	      -V '%stock-graphics-extension%=.png' \
	      --output . \
	      $(OBJ) \
	  && ln -snf $(VERBOSE) -- index.html $(notdir $(HTML)))


# - - - - - - - - - - - - - - - - - - - - - - -
# specific handling for DocBook XML documents
# - - - - - - - - - - - - - - - - - - - - - - -

.PHONY: xml-all
xml-all: xml-$(HTMLS) xml-$(TEXT) xml-$(PDF) xml-$(HTML)

.PHONY: xml-$(HTMLS)
xml-$(HTMLS): $(OUTDIR) $(OUTDIR)/images $(OUTDIR)/resources
	# -- note the mv -vu $(notdir $(HTML)) $(notdir $(HTMLS))
	#    the docbook2html processor will create a single-page
	#    HTML file called $(OBJSTEM).html, which we will want
	#    to create as a symlink, later
	(cd $(OUTDIR) \
          && XML_CATALOG_FILES="$(XML_CATALOG_FILES)" \
	      xsltproc > "$(notdir $(HTMLS))" \
	        --nonet \
	        --stringparam admon.graphics.path images/ \
	        --stringparam base.dir . \
	          "$(XSLSINGLE)" "$(OBJ)")
	# -- what about images and other resources?

.PHONY: xml-$(TEXT)
xml-$(TEXT): xml-$(HTMLS)
	(cd $(OUTDIR) && html2text -style pretty -nobs $(notdir $(HTMLS)) > $(notdir $@))

.PHONY: xml-$(FO)
xml-$(FO): $(OUTDIR)
	(cd $(OUTDIR) \
	  && XML_CATALOG_FILES=/etc/xml/catalog \
	     xsltproc > "$(notdir $(FO))" \
	        --nonet \
	          "$(XSLPRINT)" "$(OBJ)")

.PHONY: xml-$(PDF)
xml-$(PDF): xml-$(FO)
	(fop -fo $(FO) -pdf $(PDF) && rm -f $(FO) \
	 || dblatex -F xml -t pdf -o $(PDF) $(OBJ))

xml-$(HTML): xml-$(HTMLS)
	(cd $(OUTDIR) \
	  && XML_CATALOG_FILES=/etc/xml/catalog \
	      xsltproc \
	        --nonet \
	        --stringparam admon.graphics.path images/ \
	        --stringparam base.dir . \
	          "$(XSLCHUNK)" "$(OBJ)" \
	  && ln -snf $(VERBOSE) -- index.html $(notdir $(HTML)))
	# -- what about images and other resources?


# - - - - - - - - - - - - - - - - - - - - - - -
# specific handling for LinuxDoc documents
# - - - - - - - - - - - - - - - - - - - - - - -

.PHONY: linuxdoc-all
linuxdoc-all: linuxdoc-$(HTMLS) linuxdoc-$(TEXT) linuxdoc-$(PDF) linuxdoc-$(HTML)

.PHONY: linuxdoc-$(HTMLS)
linuxdoc-$(HTMLS): $(OUTDIR)/images
	# -- note the mv -vu $(notdir $(HTML)) $(notdir $(HTMLS))
	#    the docbook2html processor will create a single-page
	#    HTML file called $(OBJSTEM).html, which we will want
	#    to create as a symlink, later
	(cd $(OUTDIR) \
	  && sgml2html --split=0 $(OBJ) \
	  && mv --update $(VERBOSE) -- $(notdir $(HTML)) $(notdir $(HTMLS)))
	# -- what about images and other resources?

.PHONY: linuxdoc-$(TEXT)
linuxdoc-$(TEXT): linuxdoc-$(HTMLS)
	(cd $(OUTDIR) && html2text -style pretty -nobs $(notdir $(HTMLS)) > $(notdir $(TEXT)))

.PHONY: linuxdoc-$(PDF)
linuxdoc-$(PDF): linuxdoc-$(HTMLS)
	( cd $(OUTDIR) \
	   && htmldoc \
	        --size universal \
		-t pdf \
		--firstpage p1 \
		--outfile $(notdir $(PDF)) $(notdir $(HTMLS)))

.PHONY: linuxdoc-$(HTML)
linuxdoc-$(HTML): $(OUTDIR)
	# -- LinuxDoc processing tools create the output document file as
	#    Some-Name.html (and Some-Name-1.html, Some-Name-2.html), so we
	#    should create a symlink from index.html to the Some-Name.html.
	( cd $(OUTDIR) \
	  && sgml2html $(OBJ) \
	  && ln -snf $(VERBOSE) -- $(notdir $(HTML)) index.html)
	# -- what about images and other resources?

# - - - - - - - - - - - - - - - - - - - - - - -
# more general fragments for Makefile degubbing
# - - - - - - - - - - - - - - - - - - - - - - -

vars:
	@printf "%s\n" \
	  "OBJ       = $(OBJ)" \
	  "OBJDIR    = $(OBJDIR)" \
	  "OBJINDEX  = $(OBJINDEX)" \
	  "OBJFORMAT = $(OBJFORMAT)" \
	  "OBJFILE   = $(OBJFILE)" \
	  "OBJSTEM   = $(OBJSTEM)" \
	  "OUTDIR    = $(OUTDIR)" \
	  "PDF       = $(PDF)" \
	  "HTML      = $(HTML)" \
	  "HTMLS     = $(HTMLS)" \
	  "TEXT      = $(TEXT)" \
	  "DESTDIR   = $(DESTDIR)" \



.PHONY: help
help:
	@printf "%s\n" \
	"There will be help here in the future."

#
# -- end of file
