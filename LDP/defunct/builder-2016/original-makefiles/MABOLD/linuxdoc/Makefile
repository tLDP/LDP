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
DOCBASE    := $(WORKING)/ldp
NOWORKING  := $(shell stat 2>/dev/null -t $(WORKING))
ifeq ($(NOWORKING),)
  $(error ENOENT (2): $(WORKING); please create or specify alternate WORKING directory)
endif

VCSBASE    := /home/mabrown/vcs/LDP/LDP

#OBJ         = $(VCSBASE)/howto/linuxdoc/TransparentProxy.sgml
OBJ         = /home/mabrown/tmp/Large-Disk-HOWTO/Large-Disk-HOWTO.sgml
OBJFORMAT   = $(lastword $(subst ., ,$(suffix $(OBJ))))
OBJFILE     = $(notdir $(OBJ))
OBJSTEM     = $(OBJFILE:.$(OBJFORMAT)=)

OUTDIR      = $(DOCBASE)/$(OBJSTEM)

PDF         = $(OUTDIR)/$(OBJSTEM).pdf
HTML        = $(OUTDIR)/$(OBJSTEM).html
HTMLS       = $(OUTDIR)/$(OBJSTEM)-single.html
TEXT        = $(OUTDIR)/$(OBJSTEM).txt

all: clear_$(WORKING) $(HTMLS) $(TEXT) $(PDF) $(HTML)
	tree $(DOCBASE)
	rsync --archive --verbose --partial $(WORKING)/ $(DESTDIR)/

clear_$(WORKING):
	(test ! -d $(DOCBASE) || ( cd $(WORKING) && rm -rf -- $(notdir $(DOCBASE))))

$(DOCBASE): $(DESTDIR)
	mkdir -p $(DOCBASE)

$(OUTDIR): $(DOCBASE)
	mkdir -p $(OUTDIR)

$(HTMLS): $(OUTDIR)
	# -- note the mv -vu $(notdir $(HTML)) $(notdir $(HTMLS))
	#    the docbook2html processor will create a single-page
	#    HTML file called $(OBJSTEM).html, which we will want
	#    to create as a symlink, later
	(cd $(OUTDIR) \
          && sgml2html --split=0 $(OBJ) \
          && mv -vu $(notdir $(HTML)) $(notdir $(HTMLS)))
	# -- what about images and other resources?

$(TEXT): $(HTMLS)
	(cd $(OUTDIR) && html2text -style pretty -nobs $(notdir $(HTMLS)) > $(notdir $@))

$(PDF): $(HTMLS)
	( cd $(OUTDIR) \
          && htmldoc --size universal -t pdf --firstpage p1 --outfile $(notdir $@) $(notdir $(HTMLS)))

$(HTML): $(OUTDIR)
	# -- LinuxDoc processing tools create the output document file as
	#    Some-Name.html (and Some-Name-1.html, Some-Name-2.html), so we
	#    should create a symlink from index.html to the Some-Name.html.
	( cd $(OUTDIR) \
          && sgml2html $(OBJ) \
          && ln -snvf $(notdir $(HTML)) index.html)
	# -- what about images and other resources?

vars:
	printf "%s\n" \
	  "OBJ     = $(OBJ)" \
	  "OBJFILE = $(OBJFILE)" \
	  "OBJSTEM = $(OBJSTEM)" \
	  "DOCS    = $(DOCS)" \
	  "PDF     = $(PDF)" \
	  "HTML    = $(HTML)" \
	  "HTMLS   = $(HTMLS)" \
	  "TEXT    = $(TEXT)" \



.PHONY: help
help:
	@printf "%s\n" \
	"There will be help here in the future."

#
# -- end of file
