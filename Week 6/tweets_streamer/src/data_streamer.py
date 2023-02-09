import time
import pymongo
from faker import Faker
import tweepy


print("skript gestartet")

#client = tweepy.Client(
#    bearer_token=BEARER_TOKEN,
#    wait_on_rate_limit=True,
#)

HOST = 'mongodb'
PORT = 27017
client_mongo = pymongo.MongoClient(f"mongodb://{HOST}:{PORT}")
db = client_mongo.twitter
#logging.critical("connection established.")
#search_query = "elon musk -is:retweet -is:reply lang:en"
#fake = Faker()

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)

current_time = time.time()
while time.time() < current_time + 10:
    #fake_tweet = {"text": fake.text()}

    cursor = tweepy.Paginator(
        method=client.search_recent_tweets,
        query=search_query,
        tweet_fields=['author_id', 'created_at', 'public_metrics'],
    ).flatten(limit=20)

    for tweet in cursor:
        tweet_dict = {"text": tweet.text()}
        db.tweets.insert_one(tweet_dict)
        #with open("tweets.txt","a") as file:
        #    file.write(tweet.text+'\n')

        
    print("20 tweets written to db"+"\n")
    time.sleep(2)