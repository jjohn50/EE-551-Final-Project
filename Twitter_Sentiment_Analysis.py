#Going to need the following libraries: 
#tweepy, textblob, and some NLTK stuff 
#Used this website to help get started: 
# https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
# What I can do is use machine learning within this app that Geeks for Geeks helped with and than I can make sentiment analysis better
# Use this link: https://monkeylearn.com/blog/sentiment-analysis-of-twitter/

import re 
import tweepy 
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt 

class TwitterClient(object): 
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
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
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
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    # Right now the code will manual need to look up queury term, but I can improve this by asking the user to put something in
    search_term = input("Enter a term to look up on twitter and see how positive or negative it is ")
    print("_________________________________________________________________________________________________")

    tweets = api.get_tweets(query = search_term, count = 200) 
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))) 
    #netweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral'] 
    # code for neural tweets, but it just gives garbage 
    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:100]: 
        print(tweet['text'])       
  
    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:100]: 
        print(tweet['text']) 

    
    #I can use most of this code since its basis stuff that out there, but I can expaned upon it with the use of graphics and charts
    #Graph part: 
    #Got help from this website: https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/

    #data for the graphs

    #x values  (pos, neg, neu, total)
    type_of_tweets = ["Positive Tweets", "Negative Tweets", "Neutral Tweets"]
    # y values 
    amount_tweets = len(ptweets), len(ntweets), (len(tweets) - (len(ptweets) + len(ntweets)))

    tick_label = ["Positive Tweets", "Negative Tweets", "Neutral Tweets"]

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
    # calling main function 
    main() 

