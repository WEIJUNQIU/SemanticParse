import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
magical_class = "Nd92KSx3u2"

class WebPage(QObject):
    def __init__(self, data, parent=None):
        super(WebPage, self).__init__(parent)
        self.output = []
        self.data = data
        self.page = QWebPage()
        self.page.loadFinished.connect(self.process)

    def start(self):
        self.page.mainFrame().setHtml(self.data)

    @Slot(bool)
    def process(self, something=False):
        self.page.setViewportSize(self.page.mainFrame().contentsSize())
        frame = self.page.currentFrame()
        elements = frame.findAllElements('span[class="%s"]' % magical_class)
        for e in elements:
            s = e.toPlainText()
            rect = e.geometry()
            dim = [rect.x(), rect.y(), 
                rect.x() + rect.width(), rect.y() + rect.height()]
            if s and rect.width() > 0 and rect.height() > 0: print dim, s

if __name__ == '__main__':
    app = QApplication(sys.argv)
    webpage = WebPage('http://www.baidu.com')
    webpage.start()