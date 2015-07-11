import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re, math, time
import pickle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore, QtGui, QtWebKit

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../util/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/svm/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/adaboost/')
from common import *
from svm_model import *
from adaboost import *
from urlParse import urlParse

class MyWebView(QtWebKit.QWebPage):
    def __init__(self):
        QtWebKit.QWebPage.__init__(self)

        self.parser = urlParse()
        self.output = []
        self.input = []
        self.labels = []
        self.tem_input = []
        self.tem_labels = []
        self.content = []
        self.tagnames = []
        self.domain = ''
        self.htmlw = float(0)
        self.htmlh = float(0)
        self.tagmark = tags_mark

        self.mainFrame().loadFinished.connect(self.process)
        # self.timer = QTimer()
        # self.connect(self.timer, SIGNAL("timeout()"), self.process)
        # self.timer.start(10000)


    def process(self):
        html = self.mainFrame().documentElement()
        url = self.mainFrame().baseUrl()
        self.domain = self.parser.parse_domain(url.toString())
        self.tem_input = []
        self.tem_labels = []
        self.tagnames = []
        self.content = []
        self.htmlw = float(self.mainFrame().contentsSize().width())
        self.htmlh = float(self.mainFrame().contentsSize().height())
        print self.htmlw, self.htmlh
        if self.htmlw>0 and self.htmlh>0:
            self.get_info(html)
            if 1 in self.tem_labels:
                self.input.extend(self.tem_input)
                self.labels.extend(self.tem_labels)

        if not self.fetchNext():
            print('# soup done')
            QtGui.qApp.quit()

    def get_children(self, elem):
        echildren = []
        child = elem.firstChild()
        while not child.isNull():
            echildren.append(str(child.tagName()))
            child = child.nextSibling()
        return echildren


    def get_info(self, elem, i=0):
        if i > 200:
            return
        cnt = 0
        while cnt < 100:
            s = elem.toInnerXml()
            rect = elem.geometry()
            name = str(elem.tagName())
            attrs = elem.classes()
            eid = elem.attribute('id')

            nelem = elem.nextSibling()
            other = elem.attribute('style')
            if nelem.isNull():
                elabel = self.parser.get_label(self.domain, ' '.join([str(j) for j in attrs]), eid, '', '', other)
            else:
                nattrs = nelem.classes()
                nid = nelem.attribute('id')
                elabel = self.parser.get_label(self.domain, ' '.join([str(j) for j in attrs]), eid, ' '.join([str(j) for j in nattrs]), nid, other)

            if s and name not in ('SCRIPT', 'STYLE', 'NOSCRIPT', 'HEAD', 'FOOTER'):
                tag_mark = [k for k in self.tagmark if name.lower() in self.tagmark[k]]
                if len(tag_mark)>0:
                    tag_mark = tag_mark[0]
                else:
                    tag_mark = 0
                try:
                    self.tem_input.append([rect.x(), rect.y(), rect.width(), rect.height()])
                    class_name = ' '.join([str(j) for j in attrs])
                    self.tem_labels.append(elabel)
                    self.tagnames.append(class_name)
                    if elabel in (1, 2, 3):
                        print self.domain, 'name:', name, 'class:', ' '.join([str(j) for j in attrs]), 'id:', eid, 'label:', elabel
                except Exception, e:
                    pass
            child = elem.firstChild()
            if not child.isNull():
                self.get_info(child, i+1)
            elem = elem.nextSibling()
            if elem.isNull():
                break
            cnt += 1

    def process1(self, urls):
        self._urls = iter(urls)
        self.fetchNext()

    def fetchNext(self):
        try:
            self.mainFrame().load(QtCore.QUrl(next(self._urls)))
        except StopIteration:
            return False
        return True

if __name__=='__main__':
    count = 0
    app = QApplication(sys.argv)
    urls = open('/Users/qiuweijun/Desktop/semanticparse/predict', 'r').readlines()
    web = MyWebView()
    web.process1(urls)
    sys.exit(app.exec_())