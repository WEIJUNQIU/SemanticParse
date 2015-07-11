import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
from sklearn import preprocessing
import re, math, time, random
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtWebKit
import pickle

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../util/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/svm/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/adaboost/')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../models/nb/')

from nb_model import *
from split import *
import csv



if __name__=='__main__':
    count = 0
    for k in range(2, 9):
        csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/616/crum.csv', 'rb')
        reader = csv.reader(csvfile)
        model = Feature_Discretization()
        feature = []
        label = []
        for i in reader:
            if int(i[0]) != -1:
                feature.append(int(i[k]))
                if int(i[0]) == 1:
                    label.append(1)
                else:
                    label.append(0)
        print k, ': '
        model.fit(feature, label, 1)




