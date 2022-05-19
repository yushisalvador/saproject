from flask import Flask, render_template, request

app = Flask('app')
from waitress import serve
import tweepy
import os
import utility

api_key = os.environ['TWITTER_API_KEY']
api_secret_key = os.environ['TWITTER_API_KEY_SECRET']
access_key = os.environ['TWITTER_ACCESS_TOKEN']
access_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

try:
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
except:
    print("error in authentication")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search')
def twitter():
    return render_template("search.html")


@app.route("/tweets", methods=["POST", "GET"])
def tweets():
    if request.method == "POST":
        query = request.form["keyword"]
        count = request.form["num"]
    fetched_tweets = utility.fetch_tweets(api, query, count)
    positive = 0
    negative = 0
    neutral = 0
    count = 0
    for tweet in fetched_tweets:
        count += 1
        if tweet["sentiment"] == "positive":
            positive += 1
        if tweet["sentiment"] == "negative":
            negative += 1
        if tweet["sentiment"] == "neutral":
            neutral += 1
    positive_percentage = utility.percentage(positive, count)
    negative_percentage = utility.percentage(negative, count)
    neutral_percentage = utility.percentage(neutral, count)
    return render_template("tweets.html",
                           neu=neutral_percentage,
                           pos=positive_percentage,
                           neg=negative_percentage,
                           result=fetched_tweets)


@app.route('/phrase')
def phrase():
    return render_template('phrase.html')


@app.route('/res', methods=['POST', 'GET'])
def res():
    if request.method == 'POST':
        search_phrase = request.form['phrase']
        res = utility.analyze_phrase(search_phrase)
        neg = round(res['neg'] * 100)
        neu = round(res['neu'] * 100)
        pos = round(res['pos'] * 100)
    return render_template('phrase_result.html',
                           search_phrase=search_phrase,
                           neg=neg,
                           pos=pos,
                           neu=neu)


serve(app, host='0.0.0.0', port=8080)
