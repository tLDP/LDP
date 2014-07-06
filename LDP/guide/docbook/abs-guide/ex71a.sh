#!/bin/bash
# Same as previous example, but...

#  The - option to a here document &lt;&lt;-
#+ suppresses leading tabs in the body of the document,
#+ but *not* spaces.

cat &lt;&lt;-ENDOFMESSAGE
	This is line 1 of the message.
	This is line 2 of the message.
	This is line 3 of the message.
	This is line 4 of the message.
	This is the last line of the message.
ENDOFMESSAGE
# The output of the script will be flush left.
# Leading tab in each line will not show.

# Above 5 lines of "message" prefaced by a tab, not spaces.
# Spaces not affected by   &lt;&lt;-  .

# Note that this option has no effect on *embedded* tabs.

exit 0
