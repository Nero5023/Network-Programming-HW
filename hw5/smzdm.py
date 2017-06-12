# -*- coding: utf-8 -*-

import urllib2
from lxml import etree
from Queue import Queue
from ItemsSaver import ItemsSaver


class SMZDMSpider:
    def __init__(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.item_queue = Queue(32)
        self.item_saver_thread = ItemsSaver(self.item_queue)


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
        itemsListXPATH = "//li[@class='list']"
        allItems = root.xpath(itemsListXPATH)
        itemDatas = []
        for item in allItems:
            # Link Path
            itemLinkXPATH = "a[@href]"
            itemLinkNode = item.xpath(itemLinkXPATH)[0]
            itemLink = itemLinkNode.attrib['href']
            print "商品详情链接: ", itemLink

            # product name
            prodNameXPATH = "div[@class='listItem']/h2/a/span[@class='black']"
            prodName = item.xpath(prodNameXPATH)[0].text
            print "商品名:  ", prodName

            # price
            priceXPATH = "div[@class='listItem']/h2/a/span[@class='red']"
            price = item.xpath(priceXPATH)[0].text
            print "商品价格: ", price

            # description
            descripXPATH = "div[@class='listItem']/p"
            descrip = item.xpath(descripXPATH)[0].text
            print "商品描述: ", descrip

            # product link
            productLinkXPATH = "div[@class='listItem']/div[@class='item_buy_mall']/a"
            productLink = item.xpath(productLinkXPATH)[0].attrib['href']
            print "商品链接: ", productLink
            print "--------"
            itemDatas.append((prodName, itemLink, price, descrip, productLink))
        # put the items to the queue
        self.item_queue.put(itemDatas, 1)
        print "****************"
        pageDownLinkXPATH = "//li[@class='pagedown']/a"
        pageDownNodes = root.xpath(pageDownLinkXPATH)
        if len(pageDownNodes) == 0:
            return
        else:
            pageDownLink = pageDownNodes[0].attrib['href']
            self.getItemsInPage(pageDownLink)



    def run(self):
        firstPageURL = "http://www.smzdm.com/tag/%E4%BA%AC%E4%B8%9C618/faxian/"
        self.item_saver_thread.start()
        self.getItemsInPage(firstPageURL)


if __name__=="__main__":
    spider = SMZDMSpider()
    spider.run()
