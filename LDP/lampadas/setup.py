#!/usr/bin/env python

# FXIME, this is a template. Fill it to get it to work

""Lampadas setup script"""

from distutils.core import setup

if __name__ == '__main__' :
    setup(name="lampadas",
          version= "0.1",
          licence="GPL",
          description = "System for authoring, editing and publishing of documentation ",
          author = "David Merrill",
          author_email="david@lupercalia.net",
          url = "http://www.lampadas.org/",
          packages=['lampadas',],
          long_description = "Lampadas is a system designed to facilitate collaborative work on documentation..."
         )
											            
