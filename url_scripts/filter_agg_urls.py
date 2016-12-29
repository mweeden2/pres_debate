# created by Matt Weeden
# 12/29/16
#
# This script filters aggregate tweet urls that have no url

import sys
import csv
import time


usage = "USAGE: python filter_agg_urls.py agg_tweet_urls_file.csv"

filename = ''
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print usage
    sys.exit()


f = open(filename, 'rb')
rdr = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

lines = (r for r in rdr if r[1]!=0):

# write aggregate tweet url list
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "urls_%s.csv" % timestr
nf = open(filename, 'w')
wtr = csv.writer(nf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

for u in lines:
    wtr.writerow(u)
    nf.flush()

nf.close()
f.close()
