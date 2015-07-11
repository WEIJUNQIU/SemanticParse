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

        self.crum_input = []
        self.crum_labels = []
        self.tem_cruminput = []
        self.tem_crumlabels = []

        self.title_input = []
        self.title_labels = []
        self.tem_titleinput = []
        self.tem_titlelabels = []

        self.detail_input = []
        self.detail_labels = []
        self.tem_detailinput = []
        self.tem_detaillabels = []

        self.content = []
        self.tagnames = []
        self.domain = ''
        self.htmlw = float(0)
        self.htmlh = float(0)
        self.wordnum=0
        self.herf=0
        self.img=0

        # self.loadFinished.connect(self.process)
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.process)
        self.timer.start(20000)


    def process(self):
        html = self.page().currentFrame().documentElement()
        url = self.page().currentFrame().baseUrl()
        try:
            self.domain = self.parser.parse_domain(url.toString())
        except:
            self.domain = ''
        self.tem_cruminput = []
        self.tem_crumlabels = []
        self.tem_titleinput = []
        self.tem_titlelabels = []
        self.tem_detailinput = []
        self.tem_detaillabels = []
        self.tagnames = []
        self.content = []
        self.htmlw = float(self.page().currentFrame().contentsSize().width())
        self.htmlh = float(self.page().currentFrame().contentsSize().height())
        self.wordnum = len(html.toPlainText().replace(' ', '').replace('\n', ''))
        self.herf = html.evaluateJavaScript("""this.getElementsByTagName('a').length""").toPyObject()
        self.img = html.evaluateJavaScript("""this.getElementsByTagName('img').length""").toPyObject()
        print self.htmlw, self.htmlh, self.wordnum, self.herf, self.img
        if self.htmlw>0 and self.htmlh>0:
            try:
                self.get_info(html)
            except:
                pass
            print len(self.tem_cruminput), len(self.tem_crumlabels), len(self.tem_titleinput), len(self.tem_titlelabels), \
                len(self.tem_detailinput), len(self.tem_detaillabels)
            if 1 in self.tem_crumlabels:
                self.crum_input.extend(self.tem_cruminput)
                self.crum_labels.extend(self.tem_crumlabels)
                self.crum_input.extend([[0,0,0,0,0,0,0,0,0,0,0,0,0]])
                self.crum_labels.extend([-1])

            if 2 in self.tem_titlelabels:
                self.title_input.extend(self.tem_titleinput)
                self.title_labels.extend(self.tem_titlelabels)
                self.title_input.extend([[0,0,0,0,0,0,0,0,0,0,0,0,0]])
                self.title_labels.extend([-1])

            if 3 in self.tem_detaillabels:
                self.detail_input.extend(self.tem_detailinput)
                self.detail_labels.extend(self.tem_detaillabels)
                self.detail_input.extend([[0,0,0,0,0,0,0,0,0,0,0,0,0]])
                self.detail_labels.extend([-1])

            print len(self.crum_input), len(self.crum_labels), len(self.title_input), len(self.title_labels), \
                len(self.detail_input), len(self.detail_labels)

        # self.close()
        if not self.fetchNext():
            print('# soup done')
            QtGui.qApp.quit()

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

            if ss and name.lower() not in LEAF_TAG and rect.x() in range(-2, 150) and rect.y() in range(50, 400) and \
                            rect.width()>=100 and rect.height() in range(0, 100):
                try:
                    self.tem_cruminput.append([name, rect.x(), rect.y(), rect.width(), rect.height(), href_num, img_num,
                                                 len(s), self.htmlw, self.htmlh, self.wordnum, self.herf, self.img])
                    self.tem_crumlabels.append(elabel)
                except Exception, e:
                    pass

            if ss and name.lower() not in LEAF_TAG1 and rect.x()>=0 and rect.y() in range(50, 800) and rect.width()>=350 \
                    and rect.height() in range(50, 800):
                try:
                    self.tem_titleinput.append([name, rect.x(), rect.y(), rect.width(), rect.height(), href_num, img_num,
                                                 len(s), self.htmlw, self.htmlh, self.wordnum, self.herf, self.img])
                    self.tem_titlelabels.append(elabel)
                except Exception, e:
                    pass

            # if ' '.join([str(j) for j in attrs]) == 'fm_detail_one clearfix':
            #     print name, rect.x(), rect.y(), rect.width(), rect.height()
            if ss and name.lower() not in LEAF_TAG1 and rect.x()>=0 and rect.y()>300 and rect.width()>=300 \
                    and rect.height()>300:
                try:
                    self.tem_detailinput.append([name, rect.x(), rect.y(), rect.width(), rect.height(), href_num, img_num,
                                                 len(s), self.htmlw, self.htmlh, self.wordnum, self.herf, self.img])
                    self.tem_detaillabels.append(elabel)
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

    app = QApplication(sys.argv)
    urls = open('/Users/qiuweijun/Desktop/semanticparse/train2', 'r').readlines()
    web = MyWebView()
    web.process1(urls)
    app.exec_()

    print len(web.crum_input), len(web.crum_labels), web.crum_labels.count(1)
    print len(web.title_input), len(web.title_labels), web.title_labels.count(2)
    print len(web.detail_input), len(web.detail_labels), web.detail_labels.count(3)

    csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/new/crum1.csv', 'wb')
    writer = csv.writer(csvfile)
    for i,j in enumerate(web.crum_input):
        dd = [web.crum_labels[i]]
        dd.extend(j)
        writer.writerow(dd)

    csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/new/title1.csv', 'wb')
    writer = csv.writer(csvfile)
    for i,j in enumerate(web.title_input):
        dd = [web.title_labels[i]]
        dd.extend(j)
        writer.writerow(dd)

    csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/new/detail1.csv', 'wb')
    writer = csv.writer(csvfile)
    for i,j in enumerate(web.detail_input):
        dd = [web.detail_labels[i]]
        dd.extend(j)
        writer.writerow(dd)

    sys.exit()


