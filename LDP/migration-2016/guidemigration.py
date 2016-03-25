#! /usr/bin/python
#
# -- migrate to the new naming scheme

from __future__ import absolute_import, division, print_function

import os
import sys
import time
import errno
import shutil
import logging
import functools

logformat = '%(levelname)-9s %(name)s %(filename)s#%(lineno)s ' \
            + '%(funcName)s %(message)s'
logging.basicConfig(stream=sys.stderr, format=logformat, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -- short names
#
opa = os.path.abspath
opb = os.path.basename
opd = os.path.dirname
opj = os.path.join
opn = os.path.normpath
opr = os.path.relpath
ops = os.path.split


# -- Stem handling for HTML

predictably_named_guides = '''Bash-Beginners-Guide
cpg
espk-ug
EVMSUG
GNU-Linux-Tools-Summary
LDP-Author-Guide
Linux-Dictionary
Linux-Filesystem-Hierarchy
Linux-Media-Guide
Mobile-Guide
Pocket-Linux-Guide
sag'''.split()

stems = dict(zip(predictably_named_guides, predictably_named_guides)) 

# -- no "html" subdirectory
#
stems['lki'] = 'lki'
stems['nag2'] = 'nag2'

# -- two kernel versions, same name (in days of yore)
#
stems['lkmpg/2.4'] = 'lkmpg-2.4'
stems['lkmpg/2.6'] = 'lkmpg-2.6'

# -- wacky path naming
#
stems['lame/LAME/linux-admin-made-easy'] = 'lame'
stems['solrhe/Securing-Optimizing-Linux-RH-Edition-v1.3'] = 'solrhe'

# -- name changers
#
stems['abs'] = 'abs-guide'
stems['intro-linux'] = 'Intro-Linux'


# -- PDF handling

pdflist = '''Bash-Beginners-Guide/Bash-Beginners-Guide.pdf
EVMSUG/EVMSUG.pdf
GNU-Linux-Tools-Summary/GNU-Linux-Tools-Summary.pdf
LDP-Author-Guide/LDP-Author-Guide.pdf
Linux-Dictionary/Linux-Dictionary.pdf
Linux-Filesystem-Hierarchy/Linux-Filesystem-Hierarchy.pdf
Linux-Media-Guide/Linux-Media-Guide.pdf
Mobile-Guide/Mobile-Guide.pdf
Pocket-Linux-Guide/Pocket-Linux-Guide.pdf
cpg/Custom-Porting-Guide.pdf
espk-ug/espk-ug.pdf
lame/lame.pdf
lki/lki.pdf
nag2/nag2.pdf
sag/sag.pdf
solrhe/Securing-Optimizing-Linux-RH-Edition-v1.3.pdf'''.split()

extrapdfs = dict()
extrapdfs['lkmpg/2.4/lkmpg.pdf'] = 'lkmpg-2.4'
extrapdfs['lkmpg/2.6/lkmpg.pdf'] = 'lkmpg-2.6'
extrapdfs['abs/abs-guide.pdf'] = 'abs-guide'
extrapdfs['intro-linux/intro-linux.pdf'] = 'Intro-Linux'

def validate_args(argv):
    if len(argv) == 4:
        for d in argv[:3]:
            if not os.path.isdir(d):
                return False
        return True
    return False


def make_refresh(target, title, delay=0):
    text = '''<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>{1}: {0}</title>
    <meta http-equiv="refresh" content="{2};URL='{0}'" />
  </head>
  <body>
    <p>This page has moved permanently to 
       <a href="{0}">{0}</a>.
       Update your bookmarks if you wish.  The compatibility
       redirect will remain through, at least, early 2017.
    </p>
  </body>
</html>
'''
    return text.format(target, title, delay)

def swapfiles(a, b):
    '''use os.rename() to make "a" become "b"'''
    if not os.path.isfile(a):
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), a)
    tf = None
    if os.path.exists(b):
        _, tf = mkstemp(prefix='swapfile-', dir=opd(opa(a)))
        logger.debug("Created tempfile %s.", tf)
        logger.debug("About to rename %s to %s.", b, tf)
        os.rename(b, tf)
    logger.debug("About to rename %s to %s.", a, b)
    os.rename(a, b)
    if tf:
        logger.debug("About to rename %s to %s.", tf, a)
        os.rename(tf, a)
        logger.debug("About to remove %s.", tf)
        os.rmdir(tf)


def create_symlink(source, target):
    assert not os.path.exists(target)
    targetdir = os.path.dirname(target)
    if not os.path.isdir(targetdir):
        logger.debug("Creating directory %s", targetdir)
        os.makedirs(targetdir)
    logger.debug("Creating symlink %s, pointing to %s", target, source)
    os.symlink(os.path.relpath(source, start=targetdir), target)


def create_refresh_meta_equiv(fname, url, stem, **kwargs):
    assert not os.path.exists(fname)
    targetdir = os.path.dirname(fname)
    if not os.path.isdir(targetdir):
        logger.debug("Creating directory %s", targetdir)
        os.makedirs(targetdir)
    logger.debug("Creating file %s, with redirect to %s", fname, url)
    with open(fname, 'w') as f:
        f.write(make_refresh(url, stem, **kwargs))


def newhtmlfilename(pubdir, stem, fname):
    sought = opj(pubdir, stem, fname)
    if not os.path.isfile(sought):
        return opj(pubdir, stem, 'index.html')
    return sought

def guides(stems, guidepath, guidecompat, pubdir, urlbase):

    for pdf in pdflist:
        stem, _ = os.path.split(pdf)
        oldpdf = opj(guidecompat, pdf)
        newpdf = opj(pubdir, stem, stem + '.pdf')
        assert os.path.exists(oldpdf)
        assert os.path.exists(newpdf)
        os.rename(oldpdf, oldpdf + '.' + str(int(time.time())))
        create_symlink(newpdf, oldpdf)

    for pdf, stem in extrapdfs.items():
        oldpdf = opj(guidecompat, pdf)
        newpdf = opj(pubdir, stem, stem + '.pdf')
        assert os.path.exists(oldpdf)
        assert os.path.exists(newpdf)
        os.rename(oldpdf, oldpdf + '.' + str(int(time.time())))
        create_symlink(newpdf, oldpdf)

    for stem, newstem in sorted(stems.items(), key=lambda x: x[1].lower()):
        htmldir = opj(guidecompat, stem, 'html')
        if not os.path.isdir(htmldir):
            htmldir, _ = os.path.split(htmldir)
            assert os.path.exists(htmldir)
        for fn in os.listdir(htmldir):
            if not fn.endswith('.html'):
                continue
            pubpath = newhtmlfilename(pubdir, newstem, fn)
            url = pubpath.replace(pubdir, urlbase)
            fullname = opj(htmldir, fn)
            os.rename(fullname, fullname + '.' + str(int(time.time())))
            create_refresh_meta_equiv(fullname, url, newstem, delay=2)


def main(fin, fout, argv):
    me = os.path.basename(sys.argv[0])
    usage = "usage: %s <guidepath> <guidecompat> <pubdir> <urlbase>" % (me,)
    if not validate_args(argv):
        return usage
    guidepath, guidecompat, pubdir, urlbase = argv
    guides(stems, guidepath, guidecompat, pubdir, urlbase)
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main(sys.stdin, sys.stdout, sys.argv[1:]))

# -- end of file
