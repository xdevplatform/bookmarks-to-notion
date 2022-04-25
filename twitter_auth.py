import os
from flask import Flask, session, render_template, request
import json
import tweepy
import requests
import base64

app = Flask(__name__)

app.debug = False

app.secret_key = "super secret key"

app.config.from_pyfile('config.cfg', silent=True)

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=os.getenv('TWITTER_CLIENT_ID'),
    redirect_uri=os.getenv('TWITTER_REDIRECT_URI'),
    scope=["tweet.read", "users.read", "bookmark.read"],
    client_secret=os.getenv('TWITTER_CLIENT_SECRET'))

twitter_authorize_url = (oauth2_user_handler.get_authorization_url())


def get_tweet_ids(data):
    tweets = []
    for tweet in data:
        tweets.append(tweet['id'])
    return tweets


def get_notion_access_token(code):
    notion_client_id = os.getenv('NOTION_CLIENT_ID')
    notion_client_secret = os.getenv('NOTION_CLIENT_SECRET')
    basic_auth = notion_client_id + ":" + notion_client_secret
    params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv('NOTION_REDIRECT_URI')
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic {}".format(base64.b64encode(basic_auth.encode()).decode())
    }
    response = requests.post(url='https://api.notion.com/v1/oauth/token', data=json.dumps(params), headers=headers)
    json_response = response.json()
    if 'access_token' in json_response:
        return json_response['access_token']

# Get Notion pages
def get_pages(access_token):
    params = {
        "query": "",
        "sort": {
            "direction": "ascending",
            "timestamp": "last_edited_time"
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer {}".format(access_token)
    }
    response = requests.post(url='https://api.notion.com/v1/search', data=json.dumps(params), headers=headers)
    json_response = response.json()
    return json_response

# Create Notion page with Tweets for a user
def create_notion_page_with_tweets(access_token, page_id, tweet_ids):
    tweet_block = []
    for tweet_id in tweet_ids:
        tweet_block.append({
            "object": "block",
            "type": "embed",
            "embed": {
                "url": "https://twitter.com/s/status/{}".format(tweet_id)
            }
        })
    params = {
        "parent": {
            "page_id": page_id
        },
        "properties": {
            "title": [
                {
                    "text": {
                        "content": "Twitter Bookmarks"
                    }
                }
            ]
        },
        "children": tweet_block
    }
    headers = {
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer {}".format(access_token)
    }
    response = requests.post(url='https://api.notion.com/v1/pages', data=json.dumps(params), headers=headers)
    json_response = response.json()
    return json_response

# Get Twitter Bookmarks fro a user
def get_bookmarks(user_id, access_token):
    url = "https://api.twitter.com/2/users/{}/bookmarks?max_results=100".format(user_id)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = requests.get(url=url, headers=headers)
    return response.json()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/start')
def start():
    return render_template('start.html', authorize_url=twitter_authorize_url)

# Handle Twitter Callback
@app.route('/callback')
def callback():
    state = request.args.get('state')
    code = request.args.get('code')
    access_denied = request.args.get('error')

    if access_denied:
        return render_template('error.html', error_message="the OAuth request was denied by this user")

    twitter_redirect_uri = os.getenv('TWITTER_REDIRECT_URI')
    response_url_from_app = '{}?state={}&code={}'.format(twitter_redirect_uri, state,code)
    twitter_access_token = oauth2_user_handler.fetch_token(response_url_from_app)['access_token']
    client = tweepy.Client(twitter_access_token)
    user = client.get_me(user_auth=False, tweet_fields=['author_id'])
    id = user.data['id']
    name = user.data['name']
    bookmark_response = get_bookmarks(id, twitter_access_token)
    if 'data' in bookmark_response and len(bookmark_response['data']) > 0:
        if len(bookmark_response['data']) >= 100:
            tweet_count = '100+'
        else:
            tweet_count = len(bookmark_response['data'])
        session['tweet_ids'] = get_tweet_ids(bookmark_response['data'])
        notion_client_id = os.getenv('NOTION_CLIENT_ID')
        notion_redirect_uri = os.getenv('NOTION_REDIRECT_URI')
        authorize_url = "https://api.notion.com/v1/oauth/authorize?owner=user&client_id={}&redirect_uri={}&response_type=code".format(
            notion_client_id, notion_redirect_uri)
        return render_template('callback-success.html', name=name, tweet_count=tweet_count, authorize_url=authorize_url)
    else:
        return render_template('error.html', error_message="Unable to get Bookmarks for {}".format(name))

# Handle Notion Redirect
@app.route('/redirect')
def redirect():
    code = request.args.get('code')
    access_denied = request.args.get('error')

    if access_denied:
        return render_template('error.html', error_message="the OAuth request was denied by this user")

    if code is not None:
        notion_access_token = get_notion_access_token(code)
    else:
        return render_template('error.html', error_message="Unable to get Notion access token for this user")

    if notion_access_token is not None:
        pages = get_pages(notion_access_token)
        if 'results' in pages and len(pages['results']) > 0:
            page = pages['results'][0]
            page_id = page['id']
            if page_id is not None:
                session.pop('tweet_ids', None)
        else:
            return render_template('error.html', error_message="User did not provide permissions to any pages.")
    else:
        return render_template('error.html', error_message="Unable to get Notion access token for this user")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='uncaught exception'), 500


if __name__ == '__main__':
    app.run()
