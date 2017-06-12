# -*- coding: utf-8 -*-

import threading
import os.path
import csv
import Queue

class ItemsSaver(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.f_csv, self.f = getFileHandler()
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            try:
                rows = self.queue.get(True, 0.3)
                self.f_csv.writerows(rows)
            except Queue.Empty:
                continue

    def stop(self):
        self.f.close()
        self.stoprequest.set()

# 获取文件 handler, 当文件存在时, 以增加模式打开文件,如果不存在,则后创建文件,并写入 header
def getFileHandler():
    if not os.path.isfile("data.csv"): # not exist
        headers = ["ProductName", "ItemLink", "Price", "Description",
                    "ProductLink"]
        file = open("data.csv",'w')
        f = csv.writer(file)
        f.writerow(headers)
        return f, file
    else:
        file = open("data.csv",'a')
        f = csv.writer(file)
        return f, file
