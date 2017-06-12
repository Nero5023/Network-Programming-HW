# -*- coding: utf-8 -*-

import urllib2
from lxml import etree
import csv
import os.path


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


class SMZDMSpider:
    def __init__(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.f_csv = getFileHandler()


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
            self.saveToCSVFile(prodName, itemLink, price, descrip, productLink)
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
        self.getItemsInPage(firstPageURL)

    def saveToCSVFile(self, prodName, itemLink, price, descrip, productLink):
        row = (prodName, itemLink, price, descrip, productLink)
        self.f_csv.writerow(row)



if __name__=="__main__":
    spider = SMZDMSpider()
    spider.run()