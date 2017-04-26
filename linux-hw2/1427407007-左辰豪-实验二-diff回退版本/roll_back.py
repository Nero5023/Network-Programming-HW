# -*- coding: utf-8 -*-

import re
from collections import deque

def rollBack(originVerStr, diffInfo):
    changeTags = re.findall("\d+,?\d*[acd]\d+,?\d*", diffInfo)
    changeInfos = re.split("\n?\d+,?\d*[acd]\d+,?\d*\n", diffInfo)[1:]
    changeInfoTags = map(lambda (x,y):getOperateBeforeLinesAndOp(x,y), zip(changeTags, changeInfos))
    changedTuples = combineChangeInfoToOriginStr(originVerStr, changeInfoTags)
    # delete the some tuple
    res = filter(lambda (tag, _, target): not (tag == 'd' or tag == 'c' and target is None), changedTuples)
    res = map(lambda (x, y, target): target, res)
    res = '\n'.join(res)
    return res


# 接收 4c4   4,5c6 的信息，返回 [a,c,d] 的 index, 和对应的 changeTag
def indexOfOp(info):
    for index, ch in enumerate(info):
        if ch == 'c' or ch == 'a' or ch == 'd':
            return (index, ch)
    return None

# 接收  4c4 4,5c6 类似字符串，和字符串中的 changeTag，返回两个 range
# 第一个 range 是回滚前的行数的范围，第二个是回滚后的行数的范围，两者都是从0开始计数
def getOperatrionLines(opStr, op):
    (beforLines, afterLines) = map( lambda lines: lines.split(',') ,opStr.split(op))

    def converToRange(lineInfo):
        info = map(lambda x:int(x)-1, lineInfo)
        if len(info) == 1:
            return range(info[0], info[0]+1)
        else:
            return range(info[0], info[1]+1)
    beforLines = converToRange(beforLines)
    afterLines = converToRange(afterLines)
    return (beforLines, afterLines)


# 接收 4c4 4,5c6 类似字符串，和其后跟着的内容变化信息
# 返回3元 tuple, （回滚前的改变的行数的范围，[a,c,d]，具体变化的内容）
def getOperateBeforeLinesAndOp(opStr, chageInfo):
    (index, op) = indexOfOp(opStr)
    (beforLines, _) = getOperatrionLines(opStr, op)
    # if 
    lines = chageInfo.split('\n')
    if (op == 'c'):
        lines.remove("---")
        lines = lines[len(beforLines):]
    lines = map(lambda x: x[2:], lines)
    resLines = '\n'.join(lines)
    return (beforLines, op, resLines)

# 接收回滚前的字符串信息，和 getOperateBeforeLinesAndOp 返回的 3元 tuple 组成的数组
# 返回更具 changeOp 变化后的内容
def combineChangeInfoToOriginStr(originStr, changeInfoTags):
    linesTag = changeInfoTags
    linesTag = deque(linesTag)
    originLines = originStr.split('\n')
    res = []
    for index, lineStr in enumerate(originLines):
        # tag, changeInfo, OriginLineStr
        temp = ('','',lineStr)
        if len(linesTag) != 0:
            (tagRange, tag, chageInfo) = linesTag[0]
            if index > tagRange[-1]:
                linesTag.popleft()
                if len(linesTag) == 0:
                    continue
                (tagRange, tag, chageInfo) = linesTag[0]
            if index in tagRange:
                if tag != 'a':
                    temp = (tag, chageInfo, chageInfo)
                if tag == 'a':
                    res.append(temp)
                    temp = (tag, chageInfo, chageInfo)
                if tag == 'c':
                    linesTag[0] = (tagRange, tag, None)
        res.append(temp)
    return res


import optparse, os
def parse_args():
    usage = """ usage: %prog diffInfoFilePath originFilePath [targetFilePath]
This program is to roll back the version of origin file. It need the originFile and 
the diffInfo (diff v0.2 v0.1.1), you can enter the file path for the result to write in.
    """

    p = optparse.OptionParser(usage)

    options, args = p.parse_args()
    if len(args) != 2 and len(args) != 3:
        p.error("Please provide the diffInfoFilePath and originFilePath")
    for path in args[:2]:
        if not os.path.exists(path):
            p.error("No such file: %s" % path)
    return args

if __name__ == '__main__':
    paths = parse_args()
    targetFilePath = "target.py"
    if len(paths) == 3:
        targetFilePath = paths[2]
    with open(paths[0], 'r') as diffF, open(paths[1], 'r') as f, open(targetFilePath, 'w') as target:
        diffInfo = diffF.read()
        originVerStr = f.read()
        res = rollBack(originVerStr, diffInfo)
        target.write(res)
