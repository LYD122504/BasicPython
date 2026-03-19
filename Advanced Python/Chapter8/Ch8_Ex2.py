from follow import follow
import csv
#  Setting up a processing pipeline
lines=follow('../Data/stocklog.csv')
rows=csv.reader(lines)
for row in rows:
    print(row)
    