import mpld3
from django.shortcuts import render
from django.http import HttpResponse

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
# Bokeh Libraries
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
output_notebook()
# import plotly.express as px

import tweepy
from textblob import TextBlob

# import necessary libraries
import pandas as pd
import numpy as np
# from wordcloud import WordCloud, STOPWORDS
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Retrieving tweets from twitter
consumer_key = 'CbbklaZ4A7iOmpo9ZfsYFuWxU'
consumer_key_secret = 'RwR6OI6WVJag84B1NIk6OPCd2vv2EwFiBKpU7exePcPIDxWUZc'
access_token = '1282233149594800128-kNp1ZvypJxDLjT4A0kOKW2QjZnnBMh'
access_token_secret = 'MjvpVkdhg5MdROIMFSBDsJt0dH6a0jQFHEFKFQp2LAArb'
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

public_tweets = api.search('COVID-19', lang="en", count=100)
for tweet in public_tweets:

    print(tweet.created_at)
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    if analysis.sentiment[0] > 0:
        print("Positive")
    elif analysis.sentiment[0] < 0:
        print("Negative")
    else:
        print("Neutral")

# stopwords = set(STOPWORDS)

plt.style.use('fivethirtyeight')
i = 1
for tweet in public_tweets[0:5]:
    print(str(i) + ') ' + tweet.text + '\n')
    i = i + 1
df = pd.DataFrame([tweet.text for tweet in public_tweets], columns=['Tweets'])
df['Date'] = pd.DataFrame([tweet.created_at for tweet in public_tweets], columns=['Date'])
for i in range(df.shape[0]):
    df['Tweets'][i] = ' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\S+)|(#[A-Za-z0-9]+)", " ", df['Tweets'][i]).split()).lower()


def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity


df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

#Sentiment Analysis
def getAnalysis(score):
  if score<0:
    return 'Negative'
  elif score==0:
    return 'Neutral'
  else:
    return 'Positive'

df['Analysis']=df['Polarity'].apply(getAnalysis)


#print all the positive tweets
j=1
sortedDF=df.sort_values(by=['Polarity'])
for i in range(0,sortedDF.shape[0]):
  if(sortedDF['Analysis'][i]=='Positive'):
    print(str(j)+') '+sortedDF['Tweets'][i])
    print()
    j=j+1


def home(request):
    return render(request, 'home/index.html')
    


def about(request):
    return render(request, 'home/page4.html')
 
def news(request):
    return render(request, 'home/page1.html')

def help(request):
    return render(request, 'home/page2.html')

# def (request):
#     return render(request, 'home/.html')
# def index(request):
#     x = [1, 3, 5, 7, 9, 11, 13]
#     y = [1, 2, 3, 4, 5, 6, 7]
#     title = 'y = f(x)'

#     plot = figure(title=title,
#                   x_axis_label='X-Axis',
#                   y_axis_label='Y-Axis',
#                   plot_width=400,
#                   plot_height=400)

#     plot.line(x, y)


#     script, div = components(plot)

#     return render(request, 'home/web_home.html', {'script': script, 'div': div, })


def dash(request):
    fig = plt.figure(figsize=(10, 6))
    for i1 in range(0, df.shape[0]):
        plt.scatter(df['Polarity'][i1], df['Subjectivity'][i1], color='Blue')
    plt.title('Sentiment Analysis of COVID-19')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    # plt.show()
    sgraph = mpld3.fig_to_html(fig)

    # # percentage of positive comments
    # ptweets = df[df.Analysis == 'Positive']
    # ptweets = ptweets['Tweets']
    # round((ptweets.shape[0] / df.shape[0]) * 100, 1)

    # # percentage of negative comments
    # ntweets = df[df.Analysis == 'Negative']
    # ntweets = ntweets['Tweets']
    # round((ntweets.shape[0] / df.shape[0]) * 100, 1)

    # # percentage of neutral comments
    # neutweets = df[df.Analysis == 'Neutral']
    # neutweets = neutweets['Tweets']
    # round((neutweets.shape[0] / df.shape[0]) * 100, 1)

    # # Number of tweets per hour
    # tweets_per_hour = plt.figure(1, figsize=(10, 6))
    plt.hist(df["Date"], bins=24, color='orange');
    plt.xlabel('Hours', size=15)
    plt.ylabel('No. of Tweets', size=15)
    plt.title('No. of Tweets per Hour', size=15)

   # tgraph = mpld3.fig_to_html(tweets_per_hour)

    # seaborn

    sea_me = plt.figure(figsize=(15, 8))
    sns.distplot(df['Polarity'], bins=30, color='green')
    plt.title('Sentiment Distribution', size=25)
    plt.xlabel('Polarity', size=20)
    plt.ylabel('Frequency', size=20)
    sbgraph = mpld3.fig_to_html(sea_me)


    
    # create figure 
    p = figure(plot_width = 1200, plot_height = 550,x_axis_label='Polarity',y_axis_label='Subjectivity',title='Sentiment Analysis') 
    p.title.text_font_size = '20pt'
    p.xaxis.axis_label_text_font_size = "20pt"
    p.yaxis.axis_label_text_font_size = "20pt"
        
    # add a line renderer 
    p.hexbin(df['Polarity'],df['Subjectivity'], line_width = 5, color = "green",size=0.2, hover_color="pink", hover_alpha=0.8) 
        
    # Show the plot
    show(p)
    script1, div1 = components(p)

    #create figure
    p2 = figure(plot_width=1200, plot_height=550,x_axis_label='Date',title='Sentiment Analysis')
    p2.title.text_font_size = '20pt'
    p2.xaxis.axis_label_text_font_size = "20pt"

    # add a circle renderer with a size, color, and alpha
    p2.circle(df['Date'], df['Polarity'], size=15, color="navy", alpha=0.5)
    p2.circle(df['Date'],df['Subjectivity'],size=15, color="orange", alpha=0.5)

    # show the results
    script2, div2 = components(p2)


    p3 = figure(plot_width = 600, plot_height = 600, 
    title = 'Scatter Plot between polarity and subjectivity',
    x_axis_label = 'Polarity', y_axis_label = 'Subjectivity')
    p3.circle(df['Polarity'], df['Subjectivity'])
    # output_notebook()
    script3, div3 = components(p3)


    date=df['Date']
    polarity=df['Polarity']
    p4 = figure(x_axis_label='Tweets per hour', y_axis_label='Polarity')
    p4.line(date,polarity)
    p4.circle(date,polarity, fill_color='black', size=20)
    # output_notebook()

    script4, div4 = components(p4)
    
    bok = [  [script3, div3], [script4, div4] ]

    hor = [ [script1, div1], [script2, div2] ]




    content = {'fig': sbgraph,'hor': hor, 'bok': bok  ,'title':'Dashboard'}

    return render(request, 'home/dash.html', content) # page3
