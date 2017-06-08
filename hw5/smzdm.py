import urllib2
# f = urllib2.urlopen("http://www.smzdm.com/tag/%E4%BA%AC%E4%B8%9C618/faxian/")
# firstLine = f.read()
# print firstLine

url = "http://www.smzdm.com/tag/%E4%BA%AC%E4%B8%9C618/faxian/"
req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 \
    (Macintosh; Intel Mac OS X 10_11_6) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/58.0.3029.110 Safari/537.36')
reponse = urllib2.urlopen(req)
page = reponse.read()
print page