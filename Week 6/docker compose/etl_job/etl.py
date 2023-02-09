import pymongo
from sqlalchemy import create_engine


# Here we want to EXTRACT data from mongodb
# We then TRANSFORM the data (add value to the data)
# We finally LOAD the data into a postgres database

# connect to Mongodb
import pymongo
import time
HOST = "mongodb"
PORT = 27017
conn_string = f"mongodb://{HOST}:{PORT}"
client_mongo = pymongo.MongoClient(conn_string)

# access the twitter database
db = client_mongo.twitter
time.sleep(5)  # seconds

# Access the postgres database from python
PGUSER = "postgres"
PGPASSWORD = "postgres"
HOST = "postgresdb"
PORT = 5432
DBNAME = "twitter"
CONNECTION_STRING = f"postgresql://{PGUSER}:{PGPASSWORD}@{HOST}:{PORT}/{DBNAME}"

pg = create_engine(CONNECTION_STRING, echo=True)

# Create a postgres table for inserting transformed tweets
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')
# In case mongodb is not running in the background

#docs = db.tweets.find(limit=5)

#for doc in docs:
#    text = doc['text']
#    score = 1.0  # placeholder value
#    query = "INSERT INTO tweets VALUES (%s, %s);"
#    pg.execute(query, (text, score))
#    print(doc)

"""
# Create 3 functions:
1. extract
2. transform
3. load

apply the function
load(transform(extract()))

See below

"""

#sample_tweet
#sample_tweet

def extract():
    """
    This function extracts tweets from the mongo db
    """
    # establish connection to the mongodb
    HOST = 'mongodb'
    PORT = 27017
    client_mongo = pymongo.MongoClient(f"mongodb://{HOST}:{PORT}")
    db = client_mongo.twitter
    docs = db.tweets.find().sort("_id",pymongo.DESCENDING).limit(10)
    for doc in docs:
        print(doc)


def transform():
    """
    This tranforms the tweets by cleaning and scoring
    """
    pass

def load():
    """
    The transformed tweets must be loaded into a postgres database
    """
    pass


while True:
    extract()
    time.sleep(1)

#if __name__ == "__main__":
#    #load(transform(extract()))
#    print(extract())