from Parser import Parser 

def printDic(dic):
    for key in dic:
        print('{:15}{:3}'.format(key,dic[key]))

if __name__ == '__main__':
    p = Parser('file0.txt', 'file1.txt', 'file2.txt', 'file3.txt', 'file4.txt'\
                , 'file5.txt', 'file6.txt', 'file7.txt', 'file8.txt', 'file9.txt')
    printDic(p.parseFiles())