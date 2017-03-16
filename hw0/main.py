# -*- coding: utf-8 -*-
from Parser import Parser
import optparse
import os

def printRes(res, isDesc = None):
    if isDesc is not None:
        res = OrderedDict(sorted(res.items(), key=lambda t: t[1], reverse=isDesc))
    for key in res:
        print('{:15}{:3}'.format(key, res[key]))


def parse_args():
    usage = """ usage: %prog [options] path ...
This is the words frequency in the given files.
Run it like this:

    python main.py path0 path1 path2 ...

You can input the path or file

And it will print the words frequency in the given files or the files in the given paths.
"""
    p = optparse.OptionParser(usage)

    help = "Print the results by the order of frequency. Default is in desc order"
    p.add_option('--order', help=help)

    help = "Recursive count the files in the given path"
    p.add_option("-r", action="store_true", dest="recursive", help=help, default=False)

    options, args = p.parse_args()

    if options.order is not None:
        if options.order == "asc":
            options.order = False
        elif options.order == "desc":
            options.order = True
        else:
            p.error("--order must equal to 'asc' or 'desc")

    if len(args) == 0:
        p.error("Provide at least one file or directory")

    for path in args:
        if not os.path.exists(path):
            p.error("No such file: %s" % path)

    return options, args

from os import listdir
from os.path import isfile, join, exists
# get all the files in the given path
# It is a curry function
def filesInPath(isRec):
    def innerFunc(path):
        if not exists(path):
            return []
        if isfile(path):
            return [path]
        files = []
        for f in listdir(path):
            p = join(path, f)
            if isfile(p):
                files.append(p)
            elif isRec:
                files.extend(filesInPath(isRec)(p))
        return files
    return innerFunc


def flatMap(func, seq):
    listOfLists = map(func, seq)
    return reduce(list.__add__, listOfLists)


from collections import OrderedDict
def main():
    options, paths = parse_args()
    files = flatMap(filesInPath(options.recursive), paths)
    parser = Parser(*files)
    res = parser.parseFiles()
    printRes(res, isDesc=options.order)


if __name__ == '__main__':
    main()
