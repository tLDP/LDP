"""
Lampadas web interface

Document.
"""

#from lampadas.PresentLayer import HTMLGen XXXFIXME
from cStringIO import StringIO

# db = get_database('pgsql','ldp')

def list(req) :
	buf = StringIO()
	#HTMLGen.start_page(buf,'Welcome')
	buf.write("<h1>List of documents</h1>" % 'LDP')
	documents = db.get_documents()
	for doc in documents :
		buf.write('<p><b>%s</b><br>' % doc.title)
	#HTMLGen.end_page(buf)
	return buf.getvalue()

