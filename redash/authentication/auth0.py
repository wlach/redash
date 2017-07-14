from functools import wraps
from urllib.parse import urlparse
#from os import environ as env, path
import json

from auth0.v3.authentication import GetToken
from auth0.v3.authentication import Users
from dotenv import load_dotenv

import logging
import requests
from flask import Flask, render_template, send_from_directory, redirect, url_for, Blueprint, flash, request, session
from flask_login import login_user
from flask_oauthlib.client import OAuth
from sqlalchemy.orm.exc import NoResultFound

from redash import models, settings
from redash.authentication.org_resolving import current_org

logger = logging.getLogger('auth0')

oauth = OAuth()
blueprint = Blueprint('auth0', __name__)

def auth0_remote_app():
    if 'auth0' not in oauth.remote_apps:
        oauth.remote_app('auth0',
                         #base_url='https://www.google.com/accounts/',
                         #authorize_url='https://accounts.google.com/o/oauth2/auth',
                         #request_token_url=None,
                         #request_token_params={
                         #    'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                         #},
                         #access_token_url='https://accounts.google.com/o/oauth2/token',
                         access_token_method='POST',
                         #consumer_key=settings.GOOGLE_CLIENT_ID,
                         #consumer_secret=settings.GOOGLE_CLIENT_SECRET
                         )

    return oauth.auth0

# Controllers API

@blueprint.route('/oauth/auth0_callback', endpoint="callback")
def authorized():
    code = request.args.get(constants.CODE_KEY)
    get_token = GetToken(settings.AUTH0_DOMAIN)
    auth0_users = Users(settings.AUTH0_DOMAIN)
    token = get_token.authorization_code(settings.AUTH0_CLIENT_ID,
                                         settings.AUTH0_CLIENT_SECRET, code, settings.AUTH0_CALLBACK_URL)
    user_info = auth0_users.userinfo(token['access_token'])
    user_info_array = json.loads(user_info)
    create_and_login_user(org, user_info_array['name'], user_info_array['email'])

    next_path = request.args.get('state') or url_for("redash.index", org_slug=org.slug)

    return redirect(next_path)
