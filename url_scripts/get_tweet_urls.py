# created by Matt Weeden
# 12/15/16
#
# this script fetches tweets, viz. urls in tweets

import sys
import traceback
import tweepy
import json
import time
import csv
from random import SystemRandom


#
# make sure cmd line argument is correct
###############################################################
usage = 'usage: python get_tweet_urls.py start_at_user'
if not len(sys.argv) in [1, 2]:
    print usage
    sys.exit()

#
# set up tweepy access
###############################################################
consumer_key = "w9Pi9pM246RiVqU64eSR67U5J"
consumer_secret = "R1aCMjzYe2w0xqmdwTRTkxfegy2NoCBBn3FnhUh2Nzfam7eD2C"

access_token = "783465657878720512-NtIPcWO4Uf9BAHzuTiy9fok6f2MR7Oe"
access_token_secret = "eFq2N3IkWyER6NmaJWStGxGo75qMitHnzoA4goITScSHZ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

f = open('/home/sma2016/url_fetching/data/url_t_id.csv', 'rb')
rdr = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
t_ids = [t for t in rdr]

#
# fetch new followers_count and write to csv
###############################################################
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "/home/sma2016/url_fetching/scripts/tweet_urls_%s_r.csv" % timestr
nf = open(filename, 'w')
wtr = csv.writer(nf, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

cryptogen = SystemRandom()

#wtr.writerow(['tweet_id', 'author_id', 'number_of_urls', 'expanded_url'])

count = 0
u_count = 0
m_count = 0
nu_count = 0
while True:
    count += 1
    t = t_ids[cryptogen.randrange(len(t_ids)-1)]
    t_ids.remove(t)
    try:
        tweet = api.get_status(t[0])

        if len(tweet._json['entities']['urls']) > 0:
            urls = [u['expanded_url'] for u in tweet._json['entities']['urls']]
            wtr.writerow(t + ['%s' % len(urls)] + urls)
            nf.flush()
            u_count += 1
        else:
            nu_count += 1
            wtr.writerow(t + ['0', 'n'])
            nf.flush()
    except tweepy.error.TweepError, e:
        try:
            if 'No status found with that ID' in e.message[0]['message']:
                m_count += 1
                wtr.writerow(t + ['0', 'm'])
                nf.flush()
            else:
                print traceback.print_exc()
                wtr.writerow(t + ['0', 'err'])
        except:
            print traceback.print_exc()
            wtr.writerow(t + ['0', 'err'])
                
    if count % 3 == 0:
        sys.stdout.write('\r%s urls found of %s tweets. %s missing and %s with no url.    ' % (u_count, count, m_count, nu_count))
        sys.stdout.flush()

nf.close()
f.close()
