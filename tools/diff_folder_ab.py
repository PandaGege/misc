# -*- coding:utf-8 -*-


import os

black_files = ('.svn', '.git')
black_suffix = ('pyc',)


def diff(a, b):
    a_files = os.listdir(a)
    b_files = os.listdir(b)
    a_files = set([f for f in a_files if (f not in black_files and
                  f.split('.')[-1] not in black_suffix)])
    b_files = set([f for f in b_files if (f not in black_files and
                  f.split('.')[-1] not in black_suffix)])
    a_b = set(a_files) - set(b_files)
    b_a = set(b_files) - set(a_files)
    ab = set(a_files) & set(b_files)

    if a_b:
        print ("(%s - %s)" % (a, b)).center(79, '-')
        for f in a_b:
            print '\t', os.path.join(a, f)
        print

    if b_a:
        print ("(%s - %s)" % (b, a)).center(79, '-')
        for f in b_a:
            print '\t', os.path.join(b, f)
        print

    folders = []
    if ab:
        print ('(%s and %s) not same files' % (a, b)).center(79, '-')
        for f in ab:
            afpath = os.path.join(a, f)
            bfpath = os.path.join(b, f)
            if os.path.isfile(afpath) and os.path.isfile(bfpath):
                amd5 = os.popen('md5sum %s' % afpath).readlines()[0]\
                    .split(' ')[0]
                bmd5 = os.popen('md5sum %s' % bfpath).readlines()[0]\
                    .split(' ')[0]
                if amd5 != bmd5:
                    print '\t not same', afpath, bfpath
            elif os.path.isdir(afpath) and os.path.isdir(bfpath):
                folders.append((afpath, bfpath))
            else:
                print '\t not same', afpath, bfpath
        print

    for a, b in folders:
        diff(a, b)


if __name__ == '__main__':
    a = './diffdir/news'
    b = './news'
    diff(a, b)
