#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib2

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/crfsute/')
from bs4 import BeautifulSoup


class ListName():

    def __init__(self):
        self.tree = []

    def recursive_children(self, x):
        [x_str, b] = self.get_contents(x)
        if b:
            # details = self.segment.get_ch_words_list(x_str.replace('\n', ' '), is_merge_synonym=True)
            print x_str.replace('\n', ' ')
        else:
            for cc in x.childGenerator():
                if cc.name is not None and cc.name is not 'script':
                    self.recursive_children(cc)



    def get_contents(self, xx):
        if xx.string is not None and len(xx.string)>0:
            return [xx.string, True]
        else:
            return ['', False]

        # cont = ''
        # for cc in xx.childGenerator():
        #     if cc.string is not None and len(cc.string)>0:
        #         cont+=cc.string
        #         continue
        #     else:
        #         return ['', False]
        # if len(cont)>0:
        #     return [cont, True]
        # else:
        #     return ['', False]


if __name__ == "__main__":
    count = 0
    c = ListName()
    datas = []
    content = urllib2.urlopen('http://shijiazhuang.lashou.com/deal/11174048.htmll').read()
    # soup = BeautifulSoup(content).find(class_="w-item-info clearfix")
    # soup = BeautifulSoup(content).find(class_="w-package-deal")
    soup = BeautifulSoup(content)
    # print soup.prettify()
    if soup is not None:
        for child in soup.childGenerator():
            if child.name not in ('script', 'img') and child.name is not None:
                c.recursive_children(child)

