# created by Matt Weede
# 12/10/16
#
# This script aggregates new users "followers_count" fields from multiple csv and
#  makes a list of users yet to be fetched

import os
import sys
import csv
import time

# agg_rows[user_id] = (followers_count, date-time)
agg_rows = {}

print 'getting lists of fetched users/fcs...'
path = "../data/"
for filename in os.listdir(path):
    if filename.startswith('followers_counts') and filename.endswith('r.csv'):
        print '  ' + filename
        fn = "../data/" + filename
        f = open(fn, 'rb')
        rdr = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

        for r in rdr:
            if len(r) != 3:
                print 'There was a row with %s columns.' % len(r)
            agg_rows[r[0]] = (r[1], r[2])
        f.close()

print 'writing aggregate list...'
# write aggregate user id/followers_count list
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "agg_followers_counts_%s.csv" % timestr
nf = open(filename, 'w')
wtr = csv.writer(nf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

for u in sorted(agg_rows.keys()):
    wtr.writerow([u] + list(agg_rows[u]))
    nf.flush()
nf.close()

print 'reading old list of u_ids...'
# read complete list of user ids
f = open("../data/u_id.txt", 'rb')
all_u_ids = set()
for u in f:
    all_u_ids.add(u.strip())
f.close()

print 'writing new list of u_ids...'
# write user ids left to be fetched
nf = open('../data/u_ids_left_%s.csv' % timestr, 'w')
for u in sorted(all_u_ids - set(agg_rows.keys())):
    nf.write(u + '\n')
    nf.flush()
nf.close()
