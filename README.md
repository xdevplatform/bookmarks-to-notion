# oauth2-flask-sample



A simple Python + Flask web app that demonstrates the flow of obtaining an [access token using OAuth 2.0](https://developer.twitter.com/en/docs/basics/authentication/overview/oauth) for a Twitter user.

You can try a deployed version of the app [running on Glitch](https://oauth2-flask-sample.glitch.me/).

## Setup

1. Obtain consumer key and secret from the Twitter Developer portal. The app should be configured to enable Sign in with Twitter. See `twauth-web.py` for more details, but you can either:
   1. add these values to a `config.cfg` file (local deployment); or
   2. set environment variables `TWAUTH_APP_CONSUMER_KEY` and `TWAUTH_APP_CONSUMER_SECRET` (cloud deployment)
2. Setup a [pipenv](https://pipenv.readthedocs.io/en/latest/) environment, and install dependencies:
   1. `pipenv install`
   2. `pipenv shell`
3. Start the app:
   1. `python3 ./twauth-web.py`; or
   2. `gunicorn twauth-web:app`

> Note: the app must have an Internet-accessible URL - do not attempt to connect via localhost, as this will not work. You can run a tunnel e.g. `ngrok` for local use, or deploy to a cloud platform such as Heroku (a `Procfile` is included).

Open a browser window on your demo app's external URL. Don't click the buttons yet!

Finally, revisit the dev portal, and add your app's callback URL (`https://your-deployed-url/callback`) to the callback URL whitelist setting. Once saved, follow the instructions on the app's web UI to click through the demo pages.

## Reference

[Twitter Developer Portal](https://developer.twitter.com/)  
[Flask](https://flask.pocoo.org/)  
[python-oauth2](https://github.com/simplegeo/python-oauth2)  
[Bootstrap](https://getbootstrap.com/)  

### Credits

Original version by Jacob Petrie  
https://twitter.com/jaakkosf  
https://github.com/jaakko-sf/twauth-web  
