tables =  audience block \
	block_i18n \
	class \
	class_i18n \
	config \
	doc_vote \
	document \
	document_audience \
	document_error \
	document_file \
	document_rev \
	document_topic \
	document_user \
	document_wiki \
	dtd \
	error \
	error_i18n \
	format \
	format_i18n \
	language \
	language_i18n \
	license \
	notes \
	page \
	page_i18n \
	pub_status \
	pub_status_i18n \
	review_status \
	review_status_i18n \
	role \
	section \
	section_i18n \
	stats \
	stats_cdf \
	string \
	string_i18n \
	subtopic \
	template \
	topic \
	topic_i18n \
	username \
	username_notes

sqlprefix = /usr/local/share

INSTALLDIR = install -d
INSTALLSQL = install -p -m 644

all:	build

build:

install: all
	$(INSTALLDIR) $(sqlprefix)/lampadas
	$(INSTALLDIR) $(sqlprefix)/lampadas/sql
	for table in $(tables) ; do \
		$(INSTALLDIR) $(sqlprefix)/lampadas/sql/$$table ; \
		$(INSTALLSQL) $$table/*.sql $(sqlprefix)/lampadas/sql/$$table ; \
		$(INSTALLSQL) $$table/*.m4 $(sqlprefix)/lampadas/sql/$$table ; \
		done

clean:
	rm -f drop.sql
	rm -f create.sql
	rm -f insert.sql
	rm -f permissions.sql
	rm -f defaults.sql
	rm -f table_order.mak
	
