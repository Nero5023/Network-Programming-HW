# -*- coding: utf-8 -*-
from Parser import Parser
import optparse

def printDic(dic):
    for key in dic:
        print('{:15}{:3}'.format(key,dic[key]))

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
    p.add_option('--order', help=help, default="desc")

    help



if __name__ == '__main__':
    p = Parser('sources')
    printDic(p.parseFiles())