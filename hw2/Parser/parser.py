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


