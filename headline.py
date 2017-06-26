import feedparser
from flask import Flask
from flask import render_template,make_response
from flask import request
import json,datetime
import urllib2
import urllib

app = Flask(__name__)
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=97fdf0129bbf8b17176abf092cada2fd"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=edcc367f8a5c4aabb995de942208b05d"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc',
            'city': 'London,UK',
            'currency_from':'GBP',
            'currency_to':'USD'
}

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

@app.route("/")

@app.route("/")
def home():
    # get customized headlines, based on user input or default
    # get customised headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # get customised weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get customised currency based on user input or default
    # save cookies and return template
    response = make_response(
        render_template("home.html", articles=articles, weather=weather))
    expires = datetime.datetime.now() + datetime.timedelta(days=2)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    return response

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description':parsed['weather'][0]['description'],'temperature':parsed['main']['temp'],'city':parsed['name']}
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)