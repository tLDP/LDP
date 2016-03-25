#! /usr/bin/python
#
# -- migrate to the new naming scheme

from __future__ import absolute_import, division, print_function

import os
import sys
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

SKIP = object()


def add_renamed_stems(stems):
    stems['ppp-ssh'] = 'VPN-PPP-SSH-HOWTO'
    stems['intro-linux'] = 'Intro-Linux'
    stems['DPT-Hardware-RAID'] = 'DPT-Hardware-RAID-HOWTO'
    stems['Loadlin+Win95'] = 'Loadlin+Win95-98-ME'
    stems['Laptop-HOWTO'] = 'Mobile-Guide'
    stems['IR-HOWTO'] = 'Infrared-HOWTO'
    stems['Xnews-under-Linux-HOWTO'] = 'Windows-Newsreaders-under-Linux-HOWTO'
    stems['Access-HOWTO'] = 'Accessibility-HOWTO'
    stems['Adv-Bash-Scr-HOWTO'] = 'abs-guide'
    stems['abs'] = 'abs-guide'
    stems['Mosix-HOWTO'] = 'openMosix-HOWTO'
    stems['Partition-Rescue-New'] = 'Partition-Rescue'
    stems['Partition-Mass-Storage-Dummies-Linux-HOWTO'] = 'Partition-Mass-Storage-Definitions-Naming-HOWTO'


def add_skipped_stems(stems):
    stems['index.html'] = SKIP
    stems['INDEX'] = SKIP
    stems['README'] = SKIP
    stems['COPYRIGHT'] = SKIP
    stems['.htaccess'] = SKIP
    stems['GCC-HOWTO'] = SKIP
    stems['Netscape+Proxy'] = SKIP
    stems['Sendmail+UUCP'] = SKIP
    stems['GTEK-BBS-550'] = SKIP
    stems['Consultants-HOWTO'] = SKIP
    stems['Acer-Laptop-HOWTO'] = SKIP
    stems['Linux-From-Scratch-HOWTO'] = SKIP
    stems['Distributions-HOWTO'] = SKIP
    stems['MIPS-HOWTO'] = SKIP
    stems['3Dfx-HOWTO'] = SKIP
    stems['PostgreSQL-HOWTO'] = SKIP
    stems['Term-Firewall'] = SKIP
    stems['WikiText-HOWTO'] = SKIP
    stems['HOWTO-INDEX'] = SKIP
    stems['HOWTO-HOWTO'] = SKIP
    stems['Security-Quickstart-Redhat-HOWTO'] = SKIP


def collect_published_stems(dirbase):
    d = dict()
    for stem in os.listdir(dirbase):
        if not os.path.isdir(opj(dirbase, stem)):
            continue
        d[stem] = stem
    add_renamed_stems(d)
    add_skipped_stems(d)
    return d


def validate_args(argv):
    if len(argv) == 4:
        for d in argv[:3]:
            if not os.path.isdir(d):
                return False
        return True
    return False


def walk_simple(stems, dirbase, root):
    for name in os.listdir(dirbase):
        if name.endswith('.pdf'):
            stem, _ = os.path.splitext(name)
        else:
            stem = name
        relpath = opr(opj(dirbase, name), start=root)
        newstem = stems.get(stem, None)
        if newstem is None:
            logger.error("%s missing stem:  %s", stem, relpath)
            continue
        elif newstem is SKIP:
            logger.info("%s ignoring stem:  %s", stem, relpath)
            continue
        yield newstem, relpath


def walk_html_single(stems, dirbase, root):
    for name in os.listdir(dirbase):
        if name == 'images':
            continue
        dirname = opj(dirbase, name)
        if not os.path.isdir(dirname):
            continue
        indexhtml = opj(dirname, 'index.html')
        if not os.path.isfile(indexhtml):
            logger.error("%s missing index.html:  %s", stem, indexhtml)
        stem = name
        relpath = opr(indexhtml, start=root)
        newstem = stems.get(stem, None)
        if newstem is None:
            logger.error("%s missing stem:  %s", stem, relpath)
            continue
        elif newstem is SKIP:
            logger.info("%s ignoring stem:  %s", stem, relpath)
            continue
        yield newstem, relpath


def walk_html_chunked_dirs(stems, dirbase, root):
    for name in os.listdir(dirbase):
        if name in ('images', 'pdf', 'text', 'html_single', 'archived'):
            continue
        dirname = opj(dirbase, name)
        if not os.path.isdir(dirname):
            continue
        for subname in os.listdir(dirname):
            fname = opj(dirname, subname)
            if os.path.isdir(fname):
                continue
            stem = name
            relpath = opr(fname, start=root)
            newstem = stems.get(stem, None)
            if newstem is None:
                logger.error("%s missing stem:  %s", stem, relpath)
                continue
            elif newstem is SKIP:
                logger.info("%s ignoring stem:  %s", stem, relpath)
                continue
            yield newstem, relpath


def walk_html_chunked_files(stems, dirbase, root):
    for name in os.listdir(dirbase):
        fname = opj(dirbase, name)
        if not os.path.isfile(fname):
            continue
        stem, ext = os.path.splitext(name)
        if stem == 'index' or ext != '.html':
            continue
        if stem not in stems:
            stem = '-'.join(stem.split('-')[:-1])
            if stem not in stems:
                logger.error("Could not determine stem for %s", fname)
                continue
        relpath = opr(fname, start=root)
        newstem = stems.get(stem, None)
        if newstem is None:
            logger.error("%s missing stem:  %s", stem, relpath)
            continue
        elif newstem is SKIP:
            logger.info("%s ignoring stem:  %s", stem, relpath)
            continue
        yield newstem, relpath
            

def htmlf(stem, relpath, pubdir, newtree):
    pubf = opj(pubdir, stem, relpath)
    newf = opj(newtree, relpath)
    if os.path.exists(pubf):
        return stem, relpath, newf, pubf
    else:
        return stem, relpath, newf, opj(pubdir, stem, 'index.html')


def htmld(stem, relpath, pubdir, newtree):
    pubf = opj(pubdir, relpath)
    newf = opj(newtree, relpath)
    if os.path.exists(pubf):
        return stem, relpath, newf, pubf
    else:
        return stem, relpath, newf, opj(pubdir, stem, 'index.html')


def htmls(stem, relpath, pubdir, newtree):
    pubf = opj(pubdir, stem, stem + '-single.html')
    newf = opj(newtree, relpath)
    if os.path.exists(pubf):
        return stem, relpath, newf, pubf
    else:
        return stem, relpath, newf, opj(pubdir, stem, 'index.html')


def txt(stem, relpath, pubdir, newtree):
    pubf = opj(pubdir, stem, stem + '.txt')
    newf = opj(newtree, relpath)
    if os.path.exists(pubf):
        return stem, relpath, newf, pubf
    else:
        return stem, relpath, newf, None


def pdf(stem, relpath, pubdir, newtree):
    pubf = opj(pubdir, stem, stem + '.pdf')
    newf = opj(newtree, relpath)
    if os.path.exists(pubf):
        return stem, relpath, newf, pubf
    else:
        return stem, relpath, newf, None

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


def howtos(stems, howtopath, newtree, pubdir, urlbase):
    ldptree = dict()
    for s, r in walk_html_chunked_files(stems, howtopath, howtopath):
        ldptree[r] = htmlf(s, r, pubdir, newtree)
        # print('chunked_files', s, r)

    for s, r in walk_html_chunked_dirs(stems, howtopath, howtopath):
        ldptree[r] = htmld(s, r, pubdir, newtree)
        # print('chunked_dirs', s, r)

    howto_htmls = opj(howtopath, 'html_single')
    for s, r in walk_html_single(stems, howto_htmls, howtopath):
        ldptree[r] = htmls(s, r, pubdir, newtree)
        # print('html_single', s, r)

    for s, r in walk_simple(stems, opj(howtopath, 'text'), howtopath):
        ldptree[r] = txt(s, r, pubdir, newtree)
        # print('text', s, r)

    for s, r in walk_simple(stems, opj(howtopath, 'pdf'), howtopath):
        ldptree[r] = pdf(s, r, pubdir, newtree)
        # print('pdf', s, r)

    # -- have to symlink the PDF and TXT files
    #
    for fname in sorted(ldptree.keys(), key=lambda x: x.lower()):
        stem, relpath, newpath, pubpath = ldptree[fname]
        url = pubpath.replace(pubdir, urlbase)
        if fname.startswith('text/') or fname.startswith('pdf/'):
            create_symlink(pubpath, newpath)
        else:
            url = pubpath.replace(pubdir, urlbase)
            create_refresh_meta_equiv(newpath, url, stem, delay=2)


def main(fin, fout, argv):
    me = os.path.basename(sys.argv[0])
    usage = "usage: %s <howtopath> <howtocompat> <pubdir> <urlbase>" % (me,)
    if not validate_args(argv):
        return usage
    howtopath, howtocompat, pubdir, urlbase = argv
    oldtree = opd(opn(howtopath))

    stems = collect_published_stems(pubdir)

    howtos(stems, howtopath, howtocompat, pubdir, urlbase)
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main(sys.stdin, sys.stdout, sys.argv[1:]))

# -- end of file
