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
        files = flatMap(filesInPath, self.paths)
        for file in files:
            with open(file, 'r') as f:
                contents += " "
                contents += f.read()
        return self.parse(contents)


from os import listdir
from os.path import isfile, join, exists
# get all the files in the given path
def filesInPath(path):
    if not exists(path):
        return []
    if isfile(path):
        return [path]
    files = []
    for f in listdir(path):
        p = join(path, f)
        if isfile(p):
            files.append(p)
        else:
            files.extend(filesInPath(p))
    return files

def flatMap(func, seq):
    listOfLists = map(func, seq)
    return reduce(list.__add__, listOfLists)