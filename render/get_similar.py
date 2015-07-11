import csv
import numpy as np
import math

csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/detail.csv', 'rb')
reader = csv.reader(csvfile)

csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/detail_.csv', 'wb')
writer = csv.writer(csvfile)

count = 0
for i in reader:
    if count == 0:
        j = i
        count += 1
        continue
    elif i[0] == '3':
        tmp = (np.array([int(float(k)) for k in i[2:9]]) - np.array([int(float(k)) for k in j[2:9]])).tolist()
        if i[2:9] == j[2:9] or sum([abs(k) for k in tmp]) <= 200:
            j[0] = i[0]
        count += 1
    elif j[0] == '3':
        tmp = (np.array([int(float(k)) for k in i[2:9]]) - np.array([int(float(k)) for k in j[2:9]])).tolist()
        if i[2:9] == j[2:9] or sum([abs(k) for k in tmp]) <= 200:
            i[0] = j[0]
        count += 1
    else:
        tmp = (np.array([int(float(k)) for k in i[2:9]]) - np.array([int(float(k)) for k in j[2:9]])).tolist()
        if i[2:9] == j[2:9] or sum([abs(k) for k in tmp]) <= 200:
            j = None
        count += 1
    if j is not None:
        writer.writerow(j)
    j = i