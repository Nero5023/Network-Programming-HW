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
            print self.queue.qsize()
            rows = self.queue.get(1)
            self.f_csv.writerows(rows)

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
