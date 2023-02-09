# connecting to mongo on docker
`docker-compose exec mongodb mongo` 
- remember `mongodb` is the name of your mongodb container

## Inside mongodb, type:
`show dbs`
- you should see the twitter database
  
`use twitter`
- Switching to the twitter database

`db.tweets.find()`
- This is to see the tweets in the `tweets` collection