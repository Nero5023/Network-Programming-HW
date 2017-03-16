

# 词频统计

---------
左辰豪 1427407007


## Requirements
None

## Useage
### Basic
```python
# file
python main.py sources/file0.txt 
python main.py sources/file0.txt sources/file1.txt 

# path
python main.py sources 
```

### Print the result in order
```python
# ascending
python main.py --order=asc sources

# descending
python main.py --order=desc sources
```

### Recrusively analyze the files in given path
python main.py -r sources

## Project Structure
```
.
├── Parser
│   ├── __init__.py
│   └── parser.py
├── main.py
├── sources
│   ├── file0.txt
│   ├── file1.txt
│   ├── file2.txt
│   ├── file3.txt
│   ├── file4.txt
│   ├── file5.txt
│   ├── file6.txt
│   ├── file7.txt
│   ├── file8.txt
│   └── file9.txt
└── tests
    ├── __init__.py
    ├── context.py
    └── test_parser.py
```

## Code
### ./Parser/__init__.py
```python
from .parser import *
```

### ./Parser/parser.py
```python
from collections import Counter

class Parser(object):
    def __init__(self, *paths):
        '''paths is a list of files or dirs, it will path all files in path'''
        self.__stateStr = ""
        self.paths = paths

    # reduce iter func
    def iterParse(self, acc, x):
        if x.isalpha():
            self.__stateStr += x
            return acc
        if self.__stateStr == "":
            return acc
        acc.append(self.__stateStr)
        self.__stateStr = ""
        return acc

    def parse(self, str):
        result = reduce(self.iterParse, str, [])
        if self.__stateStr != "":
            result.append(self.__stateStr)
            self.__stateStr = ""
        return Counter(result)

    def parseFiles(self):
        contents = ""
        for file in self.paths:
            with open(file, 'r') as f:
                contents += " "
                contents += f.read()
        return self.parse(contents)
```

### ./tests/__init__.py
empty

### ./tests/context.py
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Parser import Parser 
```

### ./tests/test_parser.py
```python
from .context import Parser

import unittest

str0 = "China has proposed that North Korea suspend its tests of missile and nuclear technology to 'defuse a looming crisis'."
res0 = {'and': 1, 'a': 1, 'tests': 1, 'Korea': 1, 'North': 1, 'proposed': 1, 'that': 1, 'defuse': 1, 'of': 1, 'looming': 1, 'missile': 1, 'to': 1, 'suspend': 1, 'China': 1, 'nuclear': 1, 'has': 1, 'technology': 1, 'its': 1, 'crisis': 1}

str1 = "Hello world, Hello world, hello world,.! hello World, Hello World!"
res1 = {'world': 3, 'Hello': 3, 'World': 2, 'hello': 2}

str2 = "it was the best of times it was the worst of times it was the age of wisdom it was the age of foolishness"
res2 = {'of': 4, 'it': 4, 'the': 4, 'was': 4, 'age': 2, 'times': 2, 'foolishness': 1, 'worst': 1, 'wisdom': 1, 'best': 1}

p = Parser()

class TestParser(unittest.TestCase):

    def test_parser(self):
        self.assertTrue(p.parse(str0), res0)
        self.assertTrue(p.parse(str1), res1)
        self.assertTrue(p.parse(str2), res2)

if __name__ == '__main__':
    unittest.main()
```

### ./main.py
```python
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

```