#!/bin/bash

wall &lt;&lt;zzz23EndOfMessagezzz23
E-mail your noontime orders for pizza to the system administrator.
    (Add an extra dollar for anchovy or mushroom topping.)
# Additional message text goes here.
# Note: 'wall' prints comment lines.
zzz23EndOfMessagezzz23

# Could have been done more efficiently by
#         wall &lt;message-file
#  However, embedding the message template in a script
#+ is a quick-and-dirty one-off solution.

exit
