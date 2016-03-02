# -- Makefile for handling TLDP documentation
#
#

default: help

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
  $(error OBJ not specified, please supply a DocBook XML source file)
endif

XML_CATALOG_FILES := /etc/xml/catalog
XSLCHUNK   := /home/mabrown/vcs/LDP/LDP/builder/xsl/ldp-html-chunk.xsl
XSLSINGLE  := /home/mabrown/vcs/LDP/LDP/builder/xsl/ldp-html.xsl
XSLPRINT   := /home/mabrown/vcs/LDP/LDP/builder/xsl/ldp-print.xsl
#XSLCHUNK   := /usr/share/xml/docbook/stylesheet/ldp/html/tldp-sections.xsl
#XSLSINGLE  := /usr/share/xml/docbook/stylesheet/ldp/html/tldp-one-page.xsl
#XSLPRINT   := /usr/share/xml/docbook/stylesheet/ldp/fo/tldp-print.xsl


OBJDIR      = $(dir $(OBJ))
OBJFORMAT   = $(lastword $(subst ., ,$(suffix $(OBJ))))
OBJFILE     = $(notdir $(OBJ))
OBJSTEM     = $(OBJFILE:.$(OBJFORMAT)=)

OUTDIR      = $(abspath $(abspath $(WORKING))/$(OBJSTEM))

FO          = $(abspath $(OUTDIR)/$(OBJSTEM).fo)
PDF         = $(abspath $(OUTDIR)/$(OBJSTEM).pdf)
HTML        = $(abspath $(OUTDIR)/$(OBJSTEM).html)
HTMLS       = $(abspath $(OUTDIR)/$(OBJSTEM)-single.html)
TEXT        = $(abspath $(OUTDIR)/$(OBJSTEM).txt)

all: vars clear_$(OUTDIR) $(HTMLS) $(TEXT) $(PDF) $(HTML)
	rsync --archive --verbose --delay-updates --delete-after --partial $(OUTDIR)/ $(DESTDIR)/$(OBJSTEM)/

clear_$(OUTDIR):
	(test ! -d $(OUTDIR) || ( cd $(dir $(OUTDIR)) && rm -rf -- $(notdir $(OUTDIR))))

$(OUTDIR): $(WORKING)
	mkdir $(OUTDIR)

$(OUTDIR)/images $(OUTDIR)/resources: $(OUTDIR)
	(cd $(OBJDIR) && test ! -d $(notdir $@) || rsync -avL ./$(notdir $@) $(OUTDIR))

$(HTMLS): $(OUTDIR) $(OUTDIR)/images $(OUTDIR)/resources
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

$(TEXT): $(HTMLS)
	(cd $(OUTDIR) && html2text -style pretty -nobs $(notdir $(HTMLS)) > $(notdir $@))

$(FO): $(OUTDIR)
	( cd $(OUTDIR) \
          && XML_CATALOG_FILES=/etc/xml/catalog \
	      xsltproc > "$(notdir $(FO))" \
	        --nonet \
	          "$(XSLPRINT)" "$(OBJ)")

$(PDF): $(FO)
	(fop -fo $(FO) -pdf $(PDF) && rm -f $(FO) \
	 || dblatex -F xml -t pdf -o $(PDF) $(OBJ))

$(HTML): $(HTMLS)
	( cd $(OUTDIR) \
          && XML_CATALOG_FILES=/etc/xml/catalog \
	      xsltproc \
	        --nonet \
	        --stringparam admon.graphics.path images/ \
	        --stringparam base.dir . \
	          "$(XSLCHUNK)" "$(OBJ)" \
          && ln -snvf index.html $(notdir $(HTML)))
	# -- what about images and other resources?

vars:
	printf "%s\n" \
	  "OBJ       = $(OBJ)" \
	  "OBJFORMAT = $(OBJFORMAT)" \
	  "OBJFILE   = $(OBJFILE)" \
	  "OBJSTEM   = $(OBJSTEM)" \
	  "OUTDIR    = $(OUTDIR)" \
	  "DOCS      = $(DOCS)" \
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
