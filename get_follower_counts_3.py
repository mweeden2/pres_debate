# created by Matt Weeden
# 12/8/16
#
# this script fetches current followers_count's for a list of user id's

import sys
import tweepy
import json
import time
import csv
import logging


#
# make sure cmd line argument is correct
###############################################################
usage = 'usage: python get_follower_counts.py start_at_user'
if not len(sys.argv) in [1, 2]:
    print usage
    sys.exit()
start_num = 0
if len(sys.argv) == 2:
    try:
        start_num = int(sys.argv[1])
    except ValueError:
        print usage
        sys.exit()

#
# set up logging
###############################################################
logging.basicConfig(level=logging.INFO, filename="logfile_3.txt", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info("hello")

#
# set up tweepy access
###############################################################
consumer_key = "R6zM8waMGqly6MtxkrHyV53JP"
consumer_secret = "21SYcZDBkEMeNBCCmAwwFxLDkZqFYxhsrZ5GXyW2gOmyNcdbWR"

access_token = "783465657878720512-sIP7XvDNng7oRzHFTKedkKcPjABN1T2"
access_token_secret = "grzv0jKYFIR3xuCb3xkfLSUIJYYnBi7mZtB85cjx2xszq"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#
# read in user ids to fetch follower_count's of
###############################################################

logging.info('reading user ids...')
f = open('../data/u_id.txt', 'rb')
u_ids = []
count = 0
for i in f:
    if count >= start_num:
        u_ids.append(i.strip())
    else:
        count += 1
f.close()

#
# fetch new followers_count and write to csv
###############################################################
logging.info('fetching followers_count\'s and writing to file...')
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "followers_counts_%s_%s.csv" % (timestr, start_num)
nf = open(filename, 'w')
wtr = csv.writer(nf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

for u in u_ids:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    try:
        user = api.get_user(u)
        wtr.writerow([u, user._json['followers_count'], timestr])
    except tweepy.error.TweepError, e:
        if 'User not found' in e.message[0]['message']:
            wtr.writerow([u, 'n', timestr])
    nf.flush()

nf.close()
