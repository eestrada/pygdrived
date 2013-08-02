from __future__ import division, with_statement, print_function, unicode_literals
from future_builtins import *

import sys
import os
import webbrowser
import mimetypes
import json

import httplib2
import pprint

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import Credentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

if sys.version_info[0] == 2:
    bytes = str
    str = unicode

# Copy your credentials from the APIs Console
CLIENT_ID = '410135413619-5tqvtk7rucqtcpp7sn9fec98vkptqk4p.apps.googleusercontent.com'
CLIENT_SECRET = '4Ptfq6G0fPCwWysH2QATedGI'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
FILENAME = 'document.txt'

CONFIG_PATH = os.path.expandvars('$HOME/.config/pygdrived/credentials.json')
config_exists = os.path.exists(CONFIG_PATH)

#flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
#print(dir(flow))
#authorize_url = flow.step1_get_authorize_url()


def get_credentials():
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    #print('Go to the following link in your browser: ' + authorize_url)
    webbrowser.open(authorize_url)
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    return credentials

def get_authorized_http(credentials):
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    return http

def the_rest(http):
    drive_service = build('drive', 'v2', http=http)

    # Insert a file
    media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
    body = {
      'title': 'My document',
      'description': 'A test document',
      'mimeType': 'text/plain'
    }

    file = drive_service.files().insert(body=body, media_body=media_body).execute()
    pprint.pprint(file)

def get_config():
    if not os.path.exists(CONFIG_PATH):
        config = {}
        credentials = get_credentials()
        os.makedirs(os.path.dirname(CONFIG_PATH))

        fd = open(CONFIG_PATH, 'wt')

        fd.write(credentials.to_json())
        fd.close()

        config = credentials
    else:
        fd = open(CONFIG_PATH, 'rt')
        config = Credentials.new_from_json(fd.read())
        fd.close()

    return config

def main(args):
    credentials = get_config()
    http = get_authorized_http(credentials)
    the_rest(http)
    #jc = credentials.to_json()
    #po = json.loads(jc)
    #print(json.dumps(po, indent=4))
    return 0
