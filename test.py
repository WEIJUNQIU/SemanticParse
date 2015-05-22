#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, urllib
import nltk
import xml.etree.ElementTree as ET
from lxml import etree
import xmltodict as xt, json
import BeautifulSoup as bs
from sgmllib import SGMLParser


class ListName(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_h4 = ""
        self.name = []

    def start_h4(self, attrs):
        self.is_h4 = 1

    def end_h4(self):
        self.is_h4 = ""

    def handle_data(self, text):
        if self.is_h4 == 1:
            self.name.append(text)

content = urllib2.urlopen('http://www.nuomi.com/deal/bg3lgry3.html').read()
soup = bs.BeautifulSoup(content)
allTags = soup.body.findAll(True)
for tag in allTags:
    if tag.string is not None and len(tag.string) > 0 and tag.name != 'script':
        print tag.attrs, tag.string
        print

# print soup.body.prettify()
# root = ET.fromstring('<e> <a>text</a> <a>text</a> </e>')
# soup = bs.BeautifulSoup(''.join(content))
# print soup.find_all('title')
# listname = ListName()
# listname.feed(content)
# for item in listname.name:
#     print item.decode('gbk').encode('utf8')
