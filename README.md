# Twitter Bookmarks To Notion

A simple Python + Flask web app that demonstrates how to export Twitter Bookmarks to a Notion page.

You can try a deployed version of the app [running on Glitch](https://twitter-bookmarks-to-notion.glitch.me/).

## Setup

1. Obtain consumer key and secret from the [Twitter Developer portal](https://developer.twitter.com). The app should be configured to enable Sign in with Twitter.
2. Obtain OAuth client ID and OAuth client secret from the [Notion Developer portal](https://developers.notion.com/). See `twitter_auth.py` for more details, but you can either:
   1. add these values to a `config.cfg` file (local deployment); or
   2. set environment variables `TWITTER_CLIENT_ID` and `TWITTER_CLIENT_SECRET` (cloud deployment)
   3. set environment variables `NOTION_CLIENT_ID` and `NOTION_CLIENT_SECRET` (cloud deployment)
3. Setup a [pipenv](https://pipenv.readthedocs.io/en/latest/) environment, and install dependencies:
   1. `pipenv install`
   2. `pipenv shell`
4. Start the app:
   1. `python3 ./twitter_auth.py`; or
   2. `gunicorn twitter_auth:app`

> Note: the app must have an Internet-accessible URL - do not attempt to connect via localhost, as this will not work. You can run a tunnel e.g. `ngrok` for local use, or deploy to a cloud platform such as Heroku (a `Procfile` is included).

Open a browser window on your demo app's external URL. Don't click the buttons yet!

Finally, add the appropriate redirect URLs in developer portal for both Notion and Twitter. Also add these, as environment variables `TWITTER_REDIRECT_URI` and `NOTION_REDIRECT_URI` in your config.cfg (local deployment) or as environment variables (cloud deployment).

## Reference

[Twitter Developer Portal](https://developer.twitter.com/)  
[Notion API Docs](https://developers.notion.com/)

### Credits

Original version of Twitter OAuth login by Jacob Petrie  
https://twitter.com/jaakkosf  
https://github.com/jaakko-sf/twauth-web  
