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
  $(error OBJ not specified, please supply a LinuxDoc SGML source file)
endif

OBJFORMAT   = $(lastword $(subst ., ,$(suffix $(OBJ))))
OBJFILE     = $(notdir $(OBJ))
OBJSTEM     = $(OBJFILE:.$(OBJFORMAT)=)

OUTDIR      = $(abspath $(abspath $(WORKING))/$(OBJSTEM))

PDF         = $(abspath $(OUTDIR)/$(OBJSTEM).pdf)
HTML        = $(abspath $(OUTDIR)/$(OBJSTEM).html)
HTMLS       = $(abspath $(OUTDIR)/$(OBJSTEM)-single.html)
TEXT        = $(abspath $(OUTDIR)/$(OBJSTEM).txt)

all: vars clear_$(OUTDIR) $(HTMLS) $(TEXT) $(PDF) $(HTML)
	echo rsync --archive --verbose --delay-updates --delete-after --partial $(WORKING)/ $(DESTDIR)/

clear_$(OUTDIR):
	(test ! -d $(OUTDIR) || ( cd $(dir $(OUTDIR)) && rm -rf -- $(notdir $(OUTDIR))))

$(OUTDIR): $(WORKING)
	mkdir $(OUTDIR)

$(OUTDIR)/images: $(OUTDIR)
	(cd $(OBJDIR) && test ! -d images || rsync -avL ./images $(OUTDIR))

$(HTMLS): $(OUTDIR)/images
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
	printf "  %s\n" \
	  "OBJ       = $(OBJ)" \
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
