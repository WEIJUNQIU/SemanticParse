#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, urllib
import nltk
import xml.etree.ElementTree as ET
from lxml import etree
import xmltodict as xt, json
from bs4 import BeautifulSoup
from sgmllib import SGMLParser


class ListName():

    def __init__(self):
        self.tree = {}

    def recursive_children(self, contents):
        tags = contents.childGenerator()
        for tag in tags:
            print tag.name, tag.string
            if tag.name is not None:
                self.recursive_children(tag)
            else:
                return

    def recursive_children1(self, x):
        if x.name not in ('script', 'img'):
            if x.string is not None:
                print "[Container Node]", x.name, x.attrs, x.string.replace('\n', '')
            else:
                print "[Container Node]", x.name, x.attrs
            for cc in x.childGenerator():
                if cc.name is not None and not isinstance(cc, basestring):
                    self.recursive_children1(cc)

if __name__ == "__main__":
    # content = """
    # <html>
    # <head><title>The Dormouse's story</title></head>
    # <body>
    # <div><div>123</div></div>
    # <p class="title">
    # <b>The Dormouse's story</b>
    # <b>test</b>
    # </p>
    # <p class="story">Once upon a time there were three little sisters; and their names were
    # <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
    # <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
    # <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
    # and they lived at the bottom of a well.</p>
    # <p class="story">...</p>
    # </body>
    # </html>
    # """
    content = urllib2.urlopen('http://www.nuomi.com/deal/zne1zal0.html?s=340d2ba03968731ce6526cfafd404a61').read()

    soup = BeautifulSoup(content)
    c = ListName()
    for child in soup.body.childGenerator():
        if child.name not in ('script', 'img') and child.name is not None and child.attrs['class'][0]=='p-detail':
            print child.name, child.attrs, child.string
            c.recursive_children1(child)

    # a = 'div'
    # for child in soup.div.findAll(True):
    #     if child.name is not None:
    #         print child.name, child.string


    # tags = soup.findAll(True)
    # for tag in tags:
    #     if 'class' in tag.attrs and tag['class'][0] == 'title':
    #         print tag.name, tag['class'][0], tag.string

    # for child in soup.body.recursiveChildGenerator():
    #     if child.string is not None and len(child.string) > 0 and child.name != 'script' and child.name is not None:
    #         print child.name, child.attrs, child.string

    # for child in soup.childGenerator():
    #     ListName.recursive_children(child)

    # tags = soup.body.descendants
    # for tag in tags:
    #     if tag.string is not None and len(tag.string) > 0 and tag.name != 'script' and tag.name is not None:
    #         print tag.name, tag.string
    #         print

    # heads = soup.head.findAll(True)
    # for tag in heads:
    #     if tag.string is not None and len(tag.string) > 0 and tag.name != 'script':
    #         print tag.attrs, tag.string
    #         print
    #
    # heads = soup.body.findAll('div')
    # for tags in heads:
    #     print tags
    #     # tags_i = tags.findAll(True)
    #     # for tag in tags_i:
    #     #     if tag.string is not None and len(tag.string) > 0 and tag.name != 'script':
    #     #         print tag.name, tag.attrs, tag.string
    #     print
    #     print

    # 找出所有tags的属性和内容
    # allTags = soup.body.findAll(True)
    # for tag in allTags:
    #     if tag.string is not None and len(tag.string) > 0 and tag.name != 'script':
    #         print tag.attrs, tag.string
    #         print

    # print soup.body.prettify()
    # root = ET.fromstring('<e> <a>text</a> <a>text</a> </e>')
    # soup = bs.BeautifulSoup(''.join(content))
    # print soup.find_all('title')
    # listname = ListName()
    # listname.feed(content)
    # for item in listname.name:
    #     print item.decode('gbk').encode('utf8')
