# -*- coding: utf-8 -*-

import threading

class ItemsParser(threading.Thread):
    def __init__(self, parse_queue, save_queue):
        threading.Thread.__init__(self)
        self.parse_queue = parse_queue
        self.save_queue = save_queue

    def run(self):
        while True:
            root = self.parse_queue.get(1)
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
            self.save_queue.put(itemDatas, 1)
            print "****************"