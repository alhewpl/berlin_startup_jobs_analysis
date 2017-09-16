from nltk.corpus import twitter_samples
from nltk.tag import pos_tag_sents

tweets = twitter_samples.strings('positive_tweets.json')
tweets_tokens = twitter_samples.tokenized('positive_tweets.json')
tweets_tagged = pos_tag_sents(tweets_tokens)

JJ_count = 0
NN_count = 0

for tweet in tweets_tagged:
    for pair in tweet:
        tag = pair[1]
        if tag == 'JJ':
            JJ_count += 1
        elif tag == 'NN':
            NN_count += 1

print('Total number of adjectives = ', JJ_count)
print('Total number of nouns = ', NN_count)
#print(tweets_tokens)