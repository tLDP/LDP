#~/bin/bash

# lookup tables
psql ldp -f class.sql
psql ldp -f dtd.sql
psql ldp -f format.sql
psql ldp -f pub_status.sql
psql ldp -f review_status.sql
psql ldp -f role.sql
psql ldp -f topic.sql
psql ldp -f subtopic.sql

psql ldp -f document.sql

psql ldp -f notes.sql

psql ldp -f document_wiki.sql
psql ldp -f document_topic.sql
psql ldp -f document_rev.sql

psql ldp -f maintainer.sql
psql ldp -f maintainer_notes.sql
psql ldp -f document_maintainer.sql

psql ldp -f editor.sql
psql ldp -f editor_role.sql
psql ldp -f document_editor.sql

psql ldp -f audience.sql
psql ldp -f document_audience.sql

psql ldp -f doc_vote.sql

psql ldp -f stats.sql
psql ldp -f stats_cdf.sql

psql ldp -f license.sql

psql ldp -f volunteer.sql

psql ldp -f username.sql

#views
psql ldp -f vw_gfdl_emails.sql
psql ldp -f vw_gfdl_docs.sql
