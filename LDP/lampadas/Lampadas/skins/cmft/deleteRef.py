## Script (Python) "deleteRef"
##title=Delete a reference
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=oid, tid
REQUEST=context.REQUEST

ct = context.content_tool
ct.deleteReference(oid, tid)

return REQUEST.RESPONSE.redirect("%s/reference_edit" % ct.getObject(oid).absolute_url())
