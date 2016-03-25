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

refdocs = '''CVS-BestPractices
VideoLAN-Quickstart
VLC-User-Guide
VLS-User-Guide
INTRO/Backup-INTRO
INTRO/Intrusion-INTRO
INTRO/PhysSecurity-INTRO
INTRO/SecuringData-INTRO
INTRO/Virus-INTRO'''.split()


def validate_args(argv):
    if len(argv) == 4:
        for d in argv[:3]:
            if not os.path.isdir(d):
                return False
        return True
    return False


def collect_published_stems(dirbase):
    d = dict()
    for stem in os.listdir(dirbase):
        if not os.path.isdir(opj(dirbase, stem)):
            continue
        d[stem] = stem
    # add_renamed_stems(d)
    # add_skipped_stems(d)
    return d


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


def refs(stems, refpath, refcompat, pubdir, urlbase):

    for doc in refdocs:
        stem = doc.replace('INTRO/', '')
        if stem not in stems:
            logger.critical("Stem %s not found in %s.", stem, pubdir)
            sys.exit(1)

        # -- PDF handling
        newpdf = opj(pubdir, stem, stem + '.pdf')
        oldpdf = opj(refcompat, doc + '.pdf')
        if not os.path.exists(oldpdf):
            oldpdf = opj(refcompat, stem, stem + '.pdf')
        assert os.path.exists(oldpdf)
        assert os.path.exists(newpdf)
        os.rename(oldpdf, oldpdf + '.' + str(int(time.time())))
        create_symlink(newpdf, oldpdf)

        # -- HTML handling
        htmldir = opj(refcompat, doc, 'html')
        if not os.path.isdir(htmldir):
            htmldir, _ = os.path.split(htmldir)
            assert os.path.exists(htmldir)
        for fn in os.listdir(htmldir):
            if not fn.endswith('.html'):
                continue
            pubpath = newhtmlfilename(pubdir, stem, fn)
            url = pubpath.replace(pubdir, urlbase)
            fullname = opj(htmldir, fn)
            os.rename(fullname, fullname + '.' + str(int(time.time())))
            create_refresh_meta_equiv(fullname, url, stem, delay=2)


def main(fin, fout, argv):
    me = os.path.basename(sys.argv[0])
    usage = "usage: %s <refpath> <refcompat> <pubdir> <urlbase>" % (me,)
    if not validate_args(argv):
        return usage
    refpath, refcompat, pubdir, urlbase = argv
    stems = collect_published_stems(pubdir)
    refs(stems, refpath, refcompat, pubdir, urlbase)
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main(sys.stdin, sys.stdout, sys.argv[1:]))

# -- end of file
