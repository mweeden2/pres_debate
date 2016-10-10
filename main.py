import tweepy
import json

consumer_key = "w9Pi9pM246RiVqU64eSR67U5J"
consumer_secret = "R1aCMjzYe2w0xqmdwTRTkxfegy2NoCBBn3FnhUh2Nzfam7eD2C"

access_token = "783465657878720512-NtIPcWO4Uf9BAHzuTiy9fok6f2MR7Oe"
access_token_secret = "eFq2N3IkWyER6NmaJWStGxGo75qMitHnzoA4goITScSHZ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

f = api.followers('mweeden2')

print len(f)
for u in f:
    print u.screen_name
