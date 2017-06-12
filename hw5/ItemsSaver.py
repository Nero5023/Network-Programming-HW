# -*- coding: utf-8 -*-

import threading
import os.path
import csv
class ItemsSaver(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.f_csv = getFileHandler()

    def run(self):
        while True:
            rows = self.queue.get(1)
            self.f_csv.writerows(rows)

# 获取文件 handler, 当文件存在时, 以增加模式打开文件,如果不存在,则后创建文件,并写入 header
def getFileHandler():
    if not os.path.isfile("data.csv"): # not exist
        headers = ["ProductName", "ItemLink", "Price", "Description",
                    "ProductLink"]
        file = open("data.csv",'w')
        f = csv.writer(file)
        f.writerow(headers)
        return f
    else:
        file = open("data.csv",'a')
        f = csv.writer(file)
        return f
