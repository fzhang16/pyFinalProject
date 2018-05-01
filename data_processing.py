import json
import pandas as pd
import matplotlib.pyplot as plt
import re

#read data into an array
tweets_data_path = './tweets_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

#print len(tweets_data)

#structure the tweets data into a pandas DataFrame
tweets = pd.DataFrame()

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
# tweets['en'] = map(lambda tweet: tweet['text'] if tweet['lang'] == 'en' else None, tweets_data)

#Top 5 languages in which the tweets were written
tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

#Top 5 countries from which the tweets were sent
tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x')
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')


#return true if a word is found in text
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

tweets['cavaliers'] = tweets['text'].apply(lambda tweet: word_in_text('cavs', tweet) or word_in_text('cavaliers', tweet))
tweets['pacers'] = tweets['text'].apply(lambda tweet: word_in_text('pacers', tweet))

print tweets['cavaliers'].value_counts()[True]
print tweets['pacers'].value_counts()[True]



#compare the row data of two teams
teams = ['cavaliers', 'pacers']
tweets_by_teams = [tweets['cavaliers'].value_counts()[True], tweets['pacers'].value_counts()[True]]

x_pos = list(range(len(teams)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_teams, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('cavaliers vs. pacers', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(teams)
plt.grid()



# tweets['en'] = tweets['lang'].apply(lambda tweet: 'lang' == 'en')
# print tweets['en'].value_counts()[True]

plt.show()