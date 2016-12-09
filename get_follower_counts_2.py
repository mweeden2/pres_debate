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
from random import SystemRandom


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
logging.basicConfig(level=logging.INFO, filename="logfile_2.txt", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info("hello")

#
# set up tweepy access
###############################################################
consumer_key = "vSbf3RFFFOCrqG4rHKcIDtBuk"
consumer_secret = "PWCTCUTgNlkO4lPJHIUyzguoYBZAv4cnIb0VrbdHiLWvPFohWU"

access_token = "783465657878720512-uRnFExnBLZAjUfFXaNknCZ58TiNTkcT"
access_token_secret = "14xURp7PiaudO40nhtP9T2i6EVlu7YkDApTWSNgJt2N9o"

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
filename = "followers_counts_%s_r.csv" % timestr
nf = open(filename, 'w')
wtr = csv.writer(nf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

cryptogen = SystemRandom()
max_index = len(u_ids) - 1

while True:
    u = u_ids[cryptogen.randrange(max_index)]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    try:
        user = api.get_user(u)
        wtr.writerow([u, user._json['followers_count'], timestr])
    except tweepy.error.TweepError, e:
        if 'User not found' in e.message[0]['message']:
            wtr.writerow([u, 'n', timestr])
    nf.flush()

nf.close()
