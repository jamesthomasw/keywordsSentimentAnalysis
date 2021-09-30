import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

from developer_api_key import consumer_key, consumer_secret

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

def get_tweets(keyword):
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode='extended', lang="en").items(50):
        all_tweets.append(tweet.full_text)

    return all_tweets

def clean_tweets(all_tweets):
    clean_tweets = []
    for tweet in all_tweets:
        clean_tweets.append(p.clean(tweet))

    return clean_tweets

def calc_sentiment_score(clean_tweets):
    sentiment_score = []
    for tweet in clean_tweets:
        blob = TextBlob(tweet)
        sentiment_score.append(blob.sentiment.polarity)

    return sentiment_score

def calc_avg_sentiment_score(keyword):
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_score = calc_sentiment_score(tweets_clean)

    avg_score = statistics.mean(sentiment_score)

    return avg_score

print("Which do most people around the world prefer?")
first_keyword = input()
print("...or...")
second_keyword = input()
print("\n")

first_score = calc_avg_sentiment_score(first_keyword)
second_score = calc_avg_sentiment_score(second_keyword)

if (first_score > second_score):
    print(f'{first_keyword} is more preferable than {second_keyword}')
else:
    print(f'{second_keyword} is more preferable than {first_keyword}')
