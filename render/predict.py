import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re, math, time, csv
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore, QtGui, QtWebKit
import pickle

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../util/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/svm/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/adaboost/')
from common import *
from adaboost import *
from urlParse import urlParse

class MyWebView(QtWebKit.QWebView):
    def __init__(self):
        QtWebKit.QWebView.__init__(self)

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

        self.loadFinished.connect(self.process)
        # self.timer = QTimer()
        # self.connect(self.timer, SIGNAL("timeout()"), self.process)
        # self.timer.start(10000)


    def process(self):
        html = self.page().currentFrame().documentElement()
        url = self.page().currentFrame().baseUrl()
        self.domain = self.parser.parse_domain(url.toString())
        self.tem_input = []
        self.tem_labels = []
        self.tagnames = []
        self.content = []
        self.htmlw = float(self.page().currentFrame().contentsSize().width())
        self.htmlh = float(self.page().currentFrame().contentsSize().height())
        print self.htmlw, self.htmlh
        if self.htmlw>0 and self.htmlh>0:
            self.get_info(html)
            print len(self.tem_input), len(self.tem_labels)
            if 1 in self.tem_labels:
                self.input.extend(self.tem_input)
                self.labels.extend(self.tem_labels)
        # self.close()
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

    def sparse_count(self, num):
        if num==0:
            return 0
        else:
            return num/5+1

    def get_info(self, elem, i=0):
        if i > 200:
            return
        cnt = 0
        while cnt < 100:
            rect = elem.geometry()
            ss = elem.toInnerXml()
            s = elem.toPlainText().replace(' ', '').replace('\n', '')
            name = str(elem.tagName())
            attrs = elem.classes()
            eid = elem.attribute('id')
            nelem = elem.nextSibling()
            other = elem.attribute('style')
            href_num = elem.evaluateJavaScript("""this.getElementsByTagName('a').length""").toPyObject()
            img_num = elem.evaluateJavaScript("""this.getElementsByTagName('img').length""").toPyObject()
            if nelem.isNull():
                elabel = self.parser.get_label(self.domain, ' '.join([str(j) for j in attrs]), eid, '', '', name, other)
            else:
                nattrs = nelem.classes()
                nid = nelem.attribute('id')
                elabel = self.parser.get_label(self.domain, ' '.join([str(j) for j in attrs]), eid, ' '.join([str(j) for j in nattrs]), nid, name, other)

            if ss and name.lower() not in LEAF_TAG and rect.x()>=0 and rect.y() in range(50, 400) and rect.width()>=100 \
                    and rect.height() in range(0, 100):
                tag_mark = [k for k in self.tagmark if name.lower() in self.tagmark[k]]
                try:
                    # sparse_c = self.sparse_count(len(s))
                    self.tem_input.append([rect.x(), rect.y(), rect.width(), rect.height(), self.htmlw, self.htmlh,
                                           href_num, img_num, len(s)])
                    class_name = ' '.join([str(j) for j in attrs])
                    self.tem_labels.append(elabel)
                    self.tagnames.append(class_name)
                    if elabel in (1, 2, 3):
                        print name, 'class:', ' '.join([str(j) for j in attrs]), rect.x(), rect.y(), rect.width(), \
                            rect.height(), 'label:', elabel
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
            self.load(QtCore.QUrl(next(self._urls)))
        except StopIteration:
            return False
        return True

if __name__=='__main__':
    count = 0
    with open('crum_model.pickle', 'rb') as fp:
        model = pickle.load(fp)
    print 'load model done'

    app = QApplication(sys.argv)
    urls = open('/Users/qiuweijun/Desktop/semanticparse/d_test', 'rb').readlines()
    web = MyWebView()
    web.process1(urls)
    app.exec_()



    prob = model.predict_pro(np.array(web.input))
    mindex = 0
    mprob = 0
    content = 0
    count1 = 0
    for i in prob:
        if mprob < i[1]:
            mprob = i[1]
            mindex = count1
        count1+=1
    print len(web.input), len(web.labels)
    # print prob
    print prob[web.labels.index(3)]
    print mprob, mindex, web.tagnames[mindex], web.labels.index(1)

    sys.exit()


