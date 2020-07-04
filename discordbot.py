import discord
from discord.ext import commands
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import praw
import datetime
import random
import requests
import re
import urllib
from bs4 import BeautifulSoup


reddit = praw.Reddit(client_id='CLIENT_ID', client_secret='CLIENT_SECRET', user_agent='USER_NAME')
client = commands.Bot(command_prefix = "!")
url = ""

@client.event
async def on_read():
    print("Bot is ready!")

@client.command()
async def Hey(ctx):
    await ctx.send("Hey, you are awesome!")

@client.command()
async def btc(ctx):

    coin = getCryptoPrice(0)
    _str = "$" + str(int(coin))
    await ctx.send(_str)

@client.command()
async def eth(ctx):

    coin = getCryptoPrice(1)
    _str = "$" + str(int(coin))
    await ctx.send(_str)

@client.command()
async def ltc(ctx):

    coin = getCryptoPrice(6)
    _str = "$" + str(int(coin))
    await ctx.send(_str)

@client.command()
async def meme(ctx):

    meme = memes()
    await ctx.send(meme)

@client.command()
async def topcomment(ctx):

    comment = get_comments()
    await ctx.send(comment)


def memes():
    global url
    html_pageBoolean = True
    while html_pageBoolean:
        try:
            print("Getting URL...")
            url = get_random_meme_url(reddit)
            html_page = urllib.request.urlopen(url)
            html_pageBoolean = False
        except:
            print("Failed URL...")
            pass

    soup = BeautifulSoup(html_page, features="html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("https://i.redd.it/")}):
        imgLink = link.get('href')

        if imgLink:
            return imgLink
 
        
    
def get_random_meme_url(reddit):

    num = random.randint(0,200)
    hot = reddit.subreddit('nihilistmemes').top(limit=num)
    for submission in hot:
        url = submission.shortlink
    return url

def get_comments():
    global url
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        return top_level_comment.body


def getCryptoPrice(num):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '99b38e03-7504-4018-a71d-5a243b70facd',
    }

    session = Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data["data"][num]['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


client.run('Njk2ODA5Mjk1MzYyMjYxMDYz.XouXwg.aZdnrl62Flb-dN8kNZj98l85sdg')

