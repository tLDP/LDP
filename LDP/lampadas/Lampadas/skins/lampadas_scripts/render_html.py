from Products.CMFPlone import transaction_note

REQUEST = container.REQUEST

body = ''
l = context.objectValues(['LampadasCVSFile']) # list the objects
for i in (range(len(l))):
    sourcefile = l[i]
    body += str(sourcefile.body)
context.setBody(body)

referer = REQUEST.HTTP_REFERER
referer = context.absolute_url()

view = context.getTypeInfo().getActionById('view')
note = 'Document html has been rendered.'
transaction_note(note)

return REQUEST.RESPONSE.redirect('%s/%s?portal_status_message=%s' % ( referer
                                                                    , view
                                                                    , note) )

