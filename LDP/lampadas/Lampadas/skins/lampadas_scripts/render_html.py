#t = container.REQUEST
#RESPONSE =  request.RESPONSE

print context

body = ''
l = context.objectValues(['LampadasCVSFile']) # list the objects
for i in (range(len(l))):
    sourcefile = l[i]
    body += str(sourcefile.body)
context.setBody(body)

print 'Success.'
return printed

