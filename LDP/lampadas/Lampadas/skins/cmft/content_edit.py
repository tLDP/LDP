## Script (Python) "content_edit"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id=''
REQUEST=context.REQUEST
args = {}
formatted = {}

#new_context = context.portal_factory.doCreate(context, id, **args)

## Look for things with text_formatting
for key, value in REQUEST.form.items():
     if key.endswith("_text_format"): ##FRAGILE, depends on template
          formatted[key[:-12]] = value
     else:
          if key.endswith("_text"):
               args[key[:-5]] = value
          else:
               args[key] = value

## Pull anything with a file passed in, removing any formatting refs from before
for key, value in REQUEST.form.items():
     if key.endswith("_file"):
          filename = getattr(value, 'filename', '')
          if filename != '':
               value.seek(0)
               #new_context.set(key[:-5], value)
               context.set(key[:-5], value)               
               #Remove other formatting associated with this key
               if formatted.has_key(key[:-5]):
                    del formatted[key[:-5]]
                    del args[key[:-5]]
                    
#Set Anything complex up and remove it from the simple set
for key in formatted.keys():
     #Set things with content types
     #new_context.set(key, args[key], formatted[key])
     context.set(key, args[key], formatted[key])
     del args[key]

## EDIT the remaining fields

#new_context.edit(**args)
context.edit(**args)

#return ('success', new_context, {'portal_status_message':context.REQUEST.get('portal_status_message', 'Content changes saved.')})
return ('success', context, {'portal_status_message':context.REQUEST.get('portal_status_message', 'Content changes saved.')})
