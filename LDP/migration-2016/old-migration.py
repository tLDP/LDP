#! /usr/bin/python
#
# -- migrate to the new naming scheme

from __future__ import absolute_import, division, print_function

import os
import sys
import errno
import logging
import functools

logformat = '%(levelname)-9s %(name)s %(filename)s#%(lineno)s ' \
            + '%(funcName)s %(message)s'
logging.basicConfig(stream=sys.stderr, format=logformat,
level=logging.ERROR)
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

movingstems = dict()
movingstems['intro-linux'] = 'Intro-Linux'

def namegenerator(suffix, stem, dirname):
    fname = os.path.join(dirname, stem, stem + suffix)
    if os.path.exists(fname):
        return fname
    else:
        return None

pdf = functools.partial(namegenerator, '.pdf')
txt = functools.partial(namegenerator, '.txt')
html = functools.partial(namegenerator, '.html')
htmls = functools.partial(namegenerator, '-single.html')

def validate_args(argv):
    if len(argv) == 4:
        for d in argv[:3]:
            if not os.path.isdir(d):
                return False
        return True
    return False


def printstems(fname):
    print(fname)


def firstdir(fdir):
    if os.path.isabs(fdir):
        raise ValueError("received absolute path")
    desired = os.path.normpath(fdir)
    while os.path.sep in desired:
        desired, _ = os.path.split(desired)
    return desired


def stem_and_ext(name):
    '''return (stem, ext) for any relative or absolute filename'''
    return os.path.splitext(os.path.basename(os.path.normpath(name)))

def extract_rs_html(root, name):
    found = opj(root, name)
    relpath = opr(found, start=root)
    stem = firstdir(relpath)
    return relpath, stem


def extract_rs_htmls(root, name):
    found = opj(root, name)
    relpath = opr(found, start=opj(root, 'html_single'))
    stem = firstdir(relpath)
    return relpath, stem


def extract_relpath_and_stem(root, name):
    found = opj(root, name)
    stem, _ = stem_and_ext(found)
    relpath = opr(found, start=root)
    return relpath, stem

def extract_stem_firstdir(name, base):
    relpath = opr(name, start=base)
    stem = firstdir(relpath)
    return stem


def walktree(func, pubdir, oldtree, newtree, urlpath):
    for root, dirs, files in os.walk(oldtree):
        for x in files:
            found = os.path.join(root, x)
            relpath = os.path.relpath(found, start=oldtree)
            _, ext = stem_and_ext(found)
            if ext not in ('.pdf', '.html', '.txt'):
                if not relpath.startswith('text'):
                    func(('skip', '<stem>', '<relpath>', '<newname>', found))
                    continue
            if relpath.startswith('text') and  ext == '':
                relpath, stem = extract_relpath_and_stem(oldtree, found)
                newname = txt(stem, pubdir)
                func(('TEXT', stem, relpath, newname, found))
            elif relpath.startswith('pdf') and ext == '.pdf':
                relpath, stem = extract_relpath_and_stem(oldtree, found)
                newname = pdf(stem, pubdir)
                func(('PDF', stem, relpath, newname, found))
            elif relpath.startswith(opj(oldtree, 'html_single')):
                stem = extract_stem_firstdir(found, opj(oldtree, 'html_single'))
                newname = htmls(stem, pubdir)
                func(('HTMLS', stem, relpath, newname, found))
            elif root == oldtree:  # -- plain-files at root
                pass
            else:
                relpath, stem = extract_rs_html(oldtree, found)
                newname = html(stem, pubdir)
                func(('HTML', stem, relpath, newname, found))


def main(fin, fout, argv):
    me = os.path.basename(sys.argv[0])
    usage = "usage: %s <oldtree> <pubdir> <newtree> <urlpath>" % (me,)
    if not validate_args(argv):
        return usage
    pubdir, oldtree, newtree, urlpath = argv
    walktree(printstems, pubdir, oldtree, newtree, urlpath)
    return os.EX_OK

if __name__ == '__main__':
    sys.exit(main(sys.stdin, sys.stdout, sys.argv[1:]))

# -- end of file
