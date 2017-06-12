# -*- coding: utf-8 -*-

import urllib2
from lxml import etree
from Queue import Queue
from ItemsSaver import ItemsSaver
from ItemsParser import ItemsParser

class SMZDMSpider:
    def __init__(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.item_save_queue = Queue(32)
        self.item_parse_queue = Queue(32)
        self.item_saver_thread = ItemsSaver(self.item_save_queue)
        self.item_parse_thread = ItemsParser(self.item_parse_queue, self.item_save_queue)


    # 递归算法
    def getItemsInPage(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 \
            (Macintosh; Intel Mac OS X 10_11_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/58.0.3029.110 Safari/537.36')
        reponse = urllib2.urlopen(req)
        page = reponse.read()
        root = etree.HTML(page)
        self.item_parse_queue.put(root, 1)
        pageDownLinkXPATH = "//li[@class='pagedown']/a"
        pageDownNodes = root.xpath(pageDownLinkXPATH)
        if len(pageDownNodes) == 0:
            return
        else:
            pageDownLink = pageDownNodes[0].attrib['href']
            self.getItemsInPage(pageDownLink)



    def run(self):
        firstPageURL = "http://www.smzdm.com/tag/%E4%BA%AC%E4%B8%9C618/faxian/"
        self.item_parse_thread.start()
        self.item_saver_thread.start()
        self.getItemsInPage(firstPageURL)


if __name__=="__main__":
    spider = SMZDMSpider()
    spider.run()
