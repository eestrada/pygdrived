from __future__ import division, with_statement, print_function, unicode_literals
from future_builtins import *

import sys
import os
import io
import pwd
import getopt
import webbrowser
import mimetypes
import json
import ConfigParser

import httplib2
import pprint

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import Credentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import iohelper

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

CONFIG_PATH = os.path.expandvars('$HOME/.config/pygdrived/gdrive.cfg')
CREDENTIALS = os.path.expandvars('$HOME/.config/pygdrived/credentials.json')
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

# Workaround for ConfigParser's bad handling of unicode strings
def write_cfg(cfg, fp):
    """Write an .ini-format representation of the configuration state."""
    if not isinstance(cfg, ConfigParser.RawConfigParser):
        raise Exception('Must supply ConfigParser object.')

    if cfg.defaults():
        fp.write("[%s]\n" % 'DEFAULT')
        for (key, value) in cfg.items('DEFAULT'):
            fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
        fp.write("\n")
    for section in cfg.sections():
        fp.write("[%s]\n" % section)
        for (key, value) in cfg.items(section):
            if key not in cfg.defaults():
                fp.write("%s = %s\n" %
                         (key, str(value).replace('\n', '\n\t')))
        fp.write("\n")

def get_config():
    if not os.path.exists(CONFIG_PATH):
        cwd = os.path.abspath(os.curdir)
        os.chdir('/')
        try: os.makedirs(os.path.dirname(CONFIG_PATH))
        except Exception as e: pass
        finally: os.chdir(cwd)

        uinfo = pwd.getpwuid(os.getuid())

        defaults = {}
        defaults['sync_dir'] = os.path.join(str(uinfo.pw_dir), 'Gdrive')
        defaults['check_interval'] = str(1000) # milliseconds
        defaults['up_band_limit'] = str(-1) # bits/second
        defaults['down_band_limit'] = str(-1) # bits/second

        config = ConfigParser.SafeConfigParser(defaults)

        config.add_section('user')
        config.set('user', 'login_name', uinfo.pw_name)
        config.set('user', 'user_name', uinfo.pw_gecos)
        config.set('user', 'homedir', uinfo.pw_dir)
        config.set('user', 'shell', uinfo.pw_shell)

        config.add_section('gdrive')

        with iohelper.UnicodeIOWrapper(CONFIG_PATH, 'w') as fp:
            config.write(fp)
    else:
        config = ConfigParser.SafeConfigParser()
        with io.open(CONFIG_PATH, 'rt') as fp:
            config.readfp(fp)

    return config

def get_credentials():
    if not os.path.exists(CREDENTIALS):
        oauth_creds = {}
        credentials = get_credentials()

        cwd = os.path.abspath(os.curdir)
        os.chdir('/')
        try: os.makedirs(os.path.dirname(CREDENTIALS))
        except Exception as e: pass
        finally: os.chdir(cwd)

        with io.open(CREDENTIALS, 'wt') as fp:
            fp.write(credentials.to_json())

        oauth_creds = credentials
    else:
        with io.open(CREDENTIALS, 'rt') as fp:
            oauth_creds = Credentials.new_from_json(fp.read())

    return oauth_creds

def parse_args(argv):
    optlist, args = getopt.getopt(argv[1:], 'hvl:srk',
        ['help', 'verbose','log=', 'start', 'restart', 'kill', 'stop'])
    pass

def run_kwargs(kwargs):
    pass

def main(args):
    try:
        config = get_config()
        credentials = get_credentials()
        http = get_authorized_http(credentials)
        the_rest(http)
        #jc = credentials.to_json()
        #po = json.loads(jc)
        #print(json.dumps(po, indent=4))
    except SystemExit as e:
        raise
    else:
        raise SystemExit(0)

