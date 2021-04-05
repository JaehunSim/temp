import time

import winsound
import twitter

def repeat_sleep(seconds):
    for i in range(int(seconds*10)):
        time.sleep(0.1)
        
def make_beep():
    winsound.Beep(500, 500)
    winsound.Beep(500, 500)
    
api = twitter.Api(consumer_key="your_key",
                  consumer_secret="your_key",
                  access_token_key="your_key",
                  access_token_secret="your_key")
bearer_token = "your_key"
musk_id = 44196397

musk_recent_tweet = api.GetUserTimeline(musk_id)[0].text
index = 0
while True:
    index += 1
    if index % 100 == 0:
        print(index)
    tweet = api.GetUserTimeline(musk_id)[0].text
    if tweet != musk_recent_tweet:
        make_beep()
        musk_recent_tweet = tweet
        print(musk_recent_tweet)
    repeat_sleep(5)
