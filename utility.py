import re
import tweepy
from textblob import TextBlob
import nltk

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer




def clean_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'(@[A-Za-z0-9_]+)', '', tweet)
    tweet = re.sub('http://\S+|https://\S+', '', tweet)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    text_tokens = word_tokenize(tweet)
    tweet = [word for word in text_tokens if not word in stopwords.words()]
    tweet = ' '.join(tweet)
    return tweet


def stem(text):
    porter = PorterStemmer()
    token_words = word_tokenize(text)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(porter.stem(word))
    return " ".join(stem_sentence)


def get_tweet_sentiment(tweet):
    clean_data = clean_tweet(tweet)
    analysis = TextBlob(stem(clean_data))
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


def fetch_tweets(api, query, count=5):
    count = int(count)
    tweets = []
    try:
        fetched_tweets = tweepy.Cursor(api.search_tweets,
                                       q=query,
                                       lang='en',
                                       tweet_mode='extended').items(count)
        for tweet in fetched_tweets:
            parsed_tweet = {}
            if 'retweeted_status' in dir(tweet):
                parsed_tweet['text'] = tweet.retweeted_status.full_text
            else:
                parsed_tweet['text'] = tweet.full_text

            parsed_tweet['sentiment'] = get_tweet_sentiment(
                parsed_tweet['text'])

            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets
    except tweepy.TweepyException as e:
        print("Error : " + str(e))


def analyze_phrase(phrase):
    return SentimentIntensityAnalyzer().polarity_scores(phrase)


def percentage(part, whole):
    return 100 * float(part) / float(whole)