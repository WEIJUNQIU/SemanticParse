import csv

csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/616/detail.csv', 'rb')
reader = csv.reader(csvfile)

csvfile = file('/Users/qiuweijun/Desktop/semanticparse/data/616/detail_label.csv', 'wb')
writer = csv.writer(csvfile)

for i in reader:
    if i[0] == '3':
        tmp = [i[0], i[1], round(float(i[2].replace(',', '')), 0), round(float(i[3].replace(',', '')), 0),
               round(float(i[4].replace(',', '')), 0), round(float(i[5].replace(',', '')), 0),
               round(float(i[6].replace(',', '')), 0), round(float(i[7].replace(',', '')), 0),
               round(float(i[8].replace(',', '')), 0), round(float(i[9].replace(',', '')), 0),
               round(float(i[10].replace(',', '')), 0), round(float(i[11].replace(',', '')), 0),
               round(float(i[12].replace(',', '')), 0), round(float(i[13].replace(',', '')), 0)]
        writer.writerow(tmp)