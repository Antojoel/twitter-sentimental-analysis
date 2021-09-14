import os,tweepy,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import twitter_credentials as tc
import eel


tweetText = []

eel.init('web')


@eel.expose
def DownloadData(Searchterm,index=2):
    #authentication
    auth = tweepy.OAuthHandler(tc.CONSUMER_KEY,tc.CONSUMER_SECRET)
    auth.set_access_token(tc.ACCESS_TOKEN,tc.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    #accessing tweets
    term = 100  
    tweets = tweepy.Cursor(api.search,q=Searchterm,lang="en").items(term)

    


    #database creation
    log = open("log.txt","a")

    

    #create variable to store value
    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0

    for tweet in tweets:
        tweetText.append(clean_tweet(tweet.text).encode('UTF-8'))
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity  #adding up polarities to find the average later
    
        # adding reaction of how people are reacting to find average later
    
        if (analysis.sentiment.polarity == 0):  
                neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
            negative += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1  





    positiveper = percentage(positive,term )
    wpositiveper = percentage(wpositive, term)
    spositiveper = percentage(spositive, term)
    negativeper = percentage(negative, term)
    wnegativeper = percentage(wnegative, term)
    snegativeper = percentage(snegative, term)
    neutralper = percentage(neutral, term)   

    

    #finiding average of reaction
    polarity = polarity/term

    print("How people are reacting on " + Searchterm )
    print()
    print("General Report: ")
    if (polarity == 0):
        print("Neutral")
    elif (polarity > 0 and polarity <= 0.3):
        print("Weakly Positive")
    elif (polarity > 0.3 and polarity <= 0.6):
        print("Positive")
    elif (polarity > 0.6 and polarity <= 1):
        print("Strongly Positive")
    elif (polarity > -0.3 and polarity <= 0):
        print("Weakly Negative")
    elif (polarity > -0.6 and polarity <= -0.3):
        print("Negative")
    elif (polarity > -1 and polarity <= -0.6):
        print("Strongly Negative")

    print()
    print("Detailed Report: ")
    print(str(positiveper) + "% people thought it was positive")
    print(str(wpositiveper) + "% people thought it was weakly positive")
    print(str(spositiveper) + "% people thought it was strongly positive")
    print(str(negativeper) + "% people thought it was negative")
    print(str(wnegativeper) + "% people thought it was weakly negative")
    print(str(snegativeper) + "% people thought it was strongly negative")
    print(str(neutralper) + "% people thought it was neutral")
    


    if index==1:
        plotpiechart(positiveper, wpositiveper, spositiveper, negativeper, wnegativeper, snegativeper, neutralper, Searchterm, term)
    elif index==2:
        plotbarchart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, Searchterm, term)
    else:
        None


def clean_tweet(tweet):
    #remove un wanted from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

def percentage(part,whole):
    temp = 100*float(part)/float(whole)
    return format(temp,'.2f')


def plotpiechart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
    Sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    colours = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
    patches, texts = plt.pie(Sizes, colors=colours, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on ' + searchTerm + ' by analyzing Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show() 

def plotbarchart(positve, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noofsearchterm):
    labels = ["positve", "weakly positive", "strongly positive","neutral", "negative", "weakly negative", "strongly negative"]
    values = [positve, wpositive, spositive, neutral, negative, wnegative, snegative]
    colours = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
    plt.bar(labels,values,color=colours)
    plt.title('How people are reacting on ' + searchTerm + ' by analyzing Tweets.')
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()


eel.start('index.html')

# DownloadData(Searchterm="metoo",index=2)
