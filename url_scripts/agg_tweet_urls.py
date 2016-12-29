# created by Matt Weede
# 12/16/16
#
# This script aggregates tweet urls and makes a list of tweet_ids yet to be fetched

import os
import sys
import csv
import time

# agg_rows[tweet_id] = (author_id, num_urls, expanded_url)
agg_rows = {}

print 'getting lists of fetched tweets...'
path = "../data/"
for filename in os.listdir(path):
    if filename.startswith('tweet_urls_') and filename.endswith('r.csv'):
        print '  ' + filename
        fn = "../data/" + filename
        f = open(fn, 'rb')
        rdr = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

        for r in rdr:
            if len(r) != 3:
                print 'There was a row with %s columns.' % len(r)
                agg_rows[r[0]] = [r[i] for i in range(1, len(r))]
            else:
                agg_rows[r[0]] = [r[1], r[2]]
        f.close()

print 'writing aggregate list...'
# write aggregate tweet url list
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "agg_tweet_urls_%s.csv" % timestr
nf = open(filename, 'w')
wtr = csv.writer(nf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

for u in sorted(agg_rows.keys()):
    wtr.writerow([u] + agg_rows[u])
    nf.flush()
nf.close()

print 'reading old list of u_ids...'
# read complete list of user ids
f = open("../data/url_t_id.csv", 'rb')
rdr = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
all_t_ids = set()
for u in rdr:
    all_t_ids.add(u[0])
f.close()

print 'writing new list of u_ids...'
# write user ids left to be fetched
nf = open('../data/url_t_ids_left_%s.csv' % timestr, 'w')
for u in sorted(all_t_ids - set(agg_rows.keys())):
    nf.write(u + '\n')
    nf.flush()
nf.close()
