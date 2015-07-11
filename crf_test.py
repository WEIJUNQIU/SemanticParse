#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib2

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/crfsute/')
from bs4 import BeautifulSoup
from test_train import crfsute_train


class ListName():

    def __init__(self):
        self.tree = []

    def find_parent(self, x):
        return x.parent

    def find_presiblings(self, x):
        return x.previous_siblings

    def find_nextsiblings(self, x):
        return x.next_siblings

    def find_children(self, x):
        return x.childGenerator()

    def recursive_children(self, x):
        if x.name is not 'script':
            if x.string is not None:
                print "current", x.name, x.attrs, x.string.replace('\n', '')
                self.find_parent(x)
                self.find_presiblings(x)
                self.find_nextsiblings(x)
                self.find_children(x)
                print
            else:
                print "current", x.name, x.attrs
                self.find_parent(x)
                self.find_presiblings(x)
                self.find_nextsiblings(x)
                self.find_children(x)
                print
            for cc in x.childGenerator():
                if cc.name is not None and not isinstance(cc, basestring):
                    self.recursive_children(cc)

    def get_features(self, relation, x):
        feature = []
        for key in x.attrs:
            if key == 'class':
                feature.extend([str(relation+key+'='+x[key][0])])
            elif key=='id':
                feature.extend([str(relation+key+'='+x[key])])
        # feature.extend([str(relation+'tag_name'+'='+x.name)])
        return feature

    def recursive_children1(self, x):
        if x.name not in ('script', 'img'):
            features = []
            features.extend(self.get_features('', x))
            features.extend(self.get_features('+1:', self.find_parent(x)))
            for si in self.find_presiblings(x):
                if si.name is not None and not isinstance(si, basestring):
                    features.extend(self.get_features('0:', si))
            for si in self.find_nextsiblings(x):
                if si.name is not None and not isinstance(si, basestring):
                    features.extend(self.get_features('0:', si))
            for chi in self.find_children(x):
                if chi.name is not None and not isinstance(chi, basestring):
                    features.extend(self.get_features('-1:', chi))

            if 'class' in x.attrs:
                self.tree.append((features, ' '.join(x['class'])))
            else:
                self.tree.append((features, 'O'))
            for cc in x.childGenerator():
                if cc.name is not None and not isinstance(cc, basestring):
                    self.recursive_children1(cc)

if __name__ == "__main__":
    # content = """
    # <html cis_tag="1" class="title">
    # <head cis_tag="2"><title cis_tag="1">The Dormouse's story</title></head>
    # <body cis_tag="3">
    # <div cis_tag="4"><div cis_tag="1">123</div></div>
    # <p class="title" cis_tag="5">
    # <b cis_tag="6">The Dormouse's story</b>
    # <b cis_tag="7">test</b>
    # </p>
    # <p class="story" cis_tag="8">Once upon a time there were three little sisters; and their names were
    # <a href="http://example.com/elsie" class="sister" id="link1" cis_tag="9">Elsie</a>
    # <a href="http://example.com/lacie" class="sister" id="link2" cis_tag="10">Lacie</a>
    # <a href="http://example.com/tillie" class="sister" id="link3" cis_tag="11">Tillie</a>
    # and they lived at the bottom of a well.</p>
    # <p class="story" cis_tag="12">...</p>
    # </body>
    # </html>
    # """
    #
    # c = ListName()
    # soup = BeautifulSoup(content).body
    # c.tree = []
    # for child in soup.childGenerator():
    #     if child.name not in ('script', 'img') and child.name is not None:
    #         c.recursive_children1(child)
    # print c.tree

    count = 0
    c = ListName()
    datas = []
    lines = open('../urls', 'rb').readlines()
    for url in lines:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content).find(class_="w-item-info clearfix")
        if soup is not None:
            c.tree = []
            for child in soup.childGenerator():
                if child.name not in ('script', 'img') and child.name is not None:
                    c.recursive_children1(child)
            datas.append(c.tree)
            count+=1
            if count> 10:
                break

    model = crfsute_train()

    x_train = [[k[0] for k in s] for s in datas[0:8]]
    y_train = [[k[1] for k in s] for s in datas[0:8]]
    model.train(x_train, y_train)
    prediction = model.test(datas[9])
    print prediction
    print model.predict_prob(prediction)

    # c = ListName()
    # soup = BeautifulSoup(content)
    # for child in soup.childGenerator():
    #     if child.name not in ('script', 'img') and child.name is not None:
    #         c.recursive_children1(child)


    # X_test = [model.sent2features(s) for s in test_sents]
    # y_test = [model.sent2labels(s) for s in test_sents]
    #
    #
    # #time
    # trainer = pycrfsuite.Trainer(verbose=False)
    #
    # for xseq, yseq in zip(X_train, y_train):
    #     trainer.append(xseq, yseq)
    #
    #
    # trainer.set_params({
    #     'c1': 1.0,   # coefficient for L1 penalty
    #     'c2': 1e-3,  # coefficient for L2 penalty
    #     'max_iterations': 50,  # stop earlier
    #
    #     # include transitions that are possible, but not observed
    #     'feature.possible_transitions': True
    # })
    # trainer.params()
    #
    # #time
    # trainer.train('test.crfsuite')

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
