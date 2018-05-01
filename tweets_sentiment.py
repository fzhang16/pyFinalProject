import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser
import numpy as np

def read_scores(sent_file):
    "Parse sentiment file, returns a {word: sentiment} dict"
    with open(sent_file) as f:
        return {line.split('\t')[0]: int(line.split('\t')[1]) for line in f}


def tweet_score(tweet, scores):
    "Returns the score for a tweet or 0 if it's not in AFINN-111.txt"
    return sum(scores.get(word, 0) for word in tweet.split())


def tweet_scores(tweet_file, scores):
    "Calculate scores for all tweets in tweet_file"
    with open(tweet_file) as f:
        tweets = []
        timestamps = []
        for line in f:
            try:
                tweet = json.loads(line)
                if tweet.get('lang','') == 'en':
                    text = tweet.get('text', '')
                    if 'cavs' in text.lower() or 'cavaliers' in text.lower():
                        tweets.append(text)
                        timestamps.append(tweet.get('created_at',''))
            except:
                continue
        print len(tweets)
        score_list =[tweet_score(tweet, scores) for tweet in tweets]
        return timestamps, score_list


def data_plot(timestamps,score_list):
    data = pd.DataFrame()
    data['score'] = score_list
    # set date as pandas index
    data = data.set_index(pd.DatetimeIndex([parser.parse(d) for d in timestamps]))
    # calculate average sentiment for every 5 minutes
    data = data['score'].resample('5Min').mean()
    data.plot()
     
    plt.title('The Sentiment Change')  
    plt.xlabel('Time')  
    plt.ylabel('Sentiment')  
    plt.gcf().autofmt_xdate()
    plt.show()
    

if __name__ == '__main__':
    sent_file = "./AFINN-111.txt"
    tweet_file = "./tweets_data.txt"
    scores = read_scores(sent_file=sent_file)
    timestamps, score_list = tweet_scores(tweet_file=tweet_file, scores=scores)
    data_plot(timestamps,score_list)

    




                              