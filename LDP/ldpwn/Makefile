HOMES=/export/sunsite/users
LDPWNROOT=/public/vhost/t/tldp/html/ldpwn
LDPWNWEBROOT=http://tldp.org/ldpwn
LDPWNTO=news@en.tldp.org, lwn@lwn.net, editors@ostg.com
LDPWNCC=gferg@ibiblio.org, tille@xalasys.com, hans.bol@stork.com

all: cvsupdate render webupdate email echoedit

cvsupdate:
	@echo "Updating $(DATE).xml from CVS"
	cvs update $(DATE).xml
	@echo "done ..."
	@echo

render:
	@echo "Creating the $(DATE).html and $(DATE).txt files from $(DATE).xml"
	$(HOMES)/gferg/toolroot/ldp_mk -ldpwn $(DATE)
	@echo "$(DATE).html and $(DATE).txt created ..."
	@echo

webupdate:
	@echo "Updating the web pages at $(LDPWNROOT), adding $(DATE).html"
	cp $(DATE).html $(LDPWNROOT)
	chmod 664 $(LDPWNROOT)/$(DATE).html && chgrp ldp $(LDPWNROOT)/$(DATE).html
	cd $(LDPWNROOT) && rm latest.html && ln -s $(DATE).html latest.html
	@echo "$(DATE) can be found at $(LDPWNWEBROOT)/$(DATE).html and $(LDPWNWEBROOT)/latest.html now ..."
	@echo

email:
	@echo "Sending email with $(DATE).txt with To: $(LDPWNTO) and Cc: $(LDPWNCC)"
	cat $(DATE).txt | mail -s "The LDP Weekly News - $(DATE)" -c "$(LDPWNCC)" $(LDPWNTO)
	@echo "email sent ..."
	@echo

echoedit:
	@echo "***"
	@echo "*** Now edit $(LDPWNROOT)/index.html and add $(DATE).html"
	@echo "*** Verify that the correct $(DATE).html is linked from $(LDPWNWEBROOT)"
	@echo "*** DONT forget to copy any images to the $(LDPWNROOT) directory"
	@echo "***"
