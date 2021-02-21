#Going to need the following libraries: 
#tweepy, textblob, and some NLTK stuff 
#Used this website to help get started: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

import re 
import tweepy 
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt 
import json
import sys 

class SA(object): 
    ''' 
    Triple quotes are igonored in python
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        For the sake of protection for this program, I will need to delete the consumer key, consumer secret, etc before uploading to github
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
  
        # standard attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        This is a regex statement that clean tweet text by removing links, special characters, etc 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
          Using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # textblob will determine the sentiment of a tweet and we put it in as positive or negative
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
                                #this controls how many tweets to get
    def get_tweets(self, query, count = 2000): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, lang = "en", count = count) 
  
            # pLooks at each tweet 
            for tweet in fetched_tweets: 
                # Stores tweet here  
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    api = SA() 
    search_term = input("Enter a term to look up ")
    print("_________________________________________________________________________________________________")

    tweets = api.get_tweets(query = search_term, count = 2000) 
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print(str(search_term) + " Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print(str(search_term) + " Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print(str(search_term) + " Neutral tweets percentage: {} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))) 
    netweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral'] 
    # code for neural tweets, but it just gives garbage 

    print(str(search_term) + "\n\nPositive tweets:") 
    print("__________________________________________")
    for tweet in ptweets[:360]: 
        print(tweet['text'])       
  
    print(str(search_term) + "\n\nNegative tweets:") 
    print("__________________________________________")
    for tweet in ntweets[:360]: 
        print(tweet['text']) 

    print(str(search_term) + "\n\nNeutral  tweets:") 
    print("__________________________________________")
    for tweet in netweets[:360]: 
        print(tweet['text']) 

    #see if the item you looked up is within trending 
    consumer_key = 'ebEvVT8o3cs3C21UBxKAZF9BJ'
    consumer_secret = '1281ak3m45XuX9nYHuIDxMFRerVwrT1Lj4JXdOGJNVu1aYw71e'
    access_token = '1336373971898560516-IPYXFdQUydWOB9rnjEIdeKLguTlTTA'
    access_token_secret = 'qFU6BPvQi2kaoCL9pik8xjokAmvjSFrseAPeniNEsNHET'
    
    # authorization of consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
    # set access to user's access key and access secret  
    auth.set_access_token(access_token, access_token_secret) 
     
    # calling the api  
    api1 = tweepy.API(auth) 

    #This part of the code will allow a user to see if their selected topic is trending in New York
    print("Trending Topics Right Now in New York")
    print("_____________________________________")
    #After doing some research you need a Earth ID for special areas to get certain trending tweets
    city = input("Choose one of the cities to see if you search term is trending : New York, Los Angeles, Toronto, London, Paris, or San Francisco ")

    New_York_WOE_ID = 2459115
    Los_Angeles_WOE_ID = 2442047
    Toronto_WOE_ID = 4118
    London_WOE_ID = 44418
    Paris_WOE_ID = 615702
    San_Francisco_WOE_ID = 2487956

    if(city == "New York"):
        Trending = api1.trends_place(New_York_WOE_ID)
    elif(city == "Los Angeles"):
        Trending = api1.trends_place(Los_Angeles_WOE_ID)
    elif(city == "Toronto"):
        Trending = api1.trends_place(Toronto_WOE_ID)
    elif(city == "London"):
        Trending = api1.trends_place(London_WOE_ID)
    elif(city == "Paris"):
        Trending = api1.trends_place(Paris_WOE_ID)   
    elif(city == "San Francisco"):
        Trending = api1.trends_place(San_Francisco_WOE_ID)
    else:
        print("Enter one of the following places")

    # This code will just show trending topics in New York 
    trends = json.loads(json.dumps(Trending, indent=1))
    #The part above will parse through the data 
    for trend in trends[0]["trends"]:
        print((trend["name"]).strip("#"))

    #This code will show trending topics if they match the search term
    for trend in trends[0]["trends"]:
        if(search_term == (trend["name"]).strip("#")):
            print("The search term " + search_term + " is trending on Twitter right now ")   

    #Graph part: 
    #Got help from this website: https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/

    #data for the graphs

    #x values  (pos, neg, neu, total)
    type_of_tweets = [str(search_term) + " Positive Tweets", str(search_term)+ " Negative Tweets", str(search_term) + "Neutral Tweets"]
    # y values 
    amount_tweets = len(ptweets), len(ntweets), (len(tweets) - (len(ptweets) + len(ntweets)))

    tick_label = [str(search_term) + " Positive Tweets", str(search_term) + " Negative Tweets", str(search_term) + " Neutral Tweets"]

    #plotting of the graph
    plt.bar(type_of_tweets, amount_tweets, tick_label = tick_label, width = 0.8, color = ['Blue', 'Red', 'Gray'])
    
    #creates x label
    plt.xlabel("Types of Tweets")
    #creates y label 
    plt.ylabel("Amount of Tweets")
    #creates title 
    plt.title("Tweets vs Type of Tweets")
    #displays the graph 
    plt.show()

if __name__ == "__main__": 
    main() 
