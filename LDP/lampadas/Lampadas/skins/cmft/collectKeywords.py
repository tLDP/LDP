## Script (Python) "collectKeywords"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=name, index
REQUEST=context.REQUEST

field   = context.getField(name)

allowed = field.Vocabulary(context)
enforce = field.enforceVocabulary
    
previous = container.portal_catalog.uniqueValuesFor(index)

if enforce:
    result = allowed
else:
    result = allowed + previous


result = result.sortedByValue()
return result
