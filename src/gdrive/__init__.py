import os
import webbrowser
import mimetypes
import pickle
import json

#import httplib2
import pprint

#from apiclient.discovery import build
#from apiclient.http import MediaFileUpload
#from oauth2client.client import OAuth2WebServerFlow


# Copy your credentials from the APIs Console
CLIENT_ID = '410135413619-5tqvtk7rucqtcpp7sn9fec98vkptqk4p.apps.googleusercontent.com'
CLIENT_SECRET = '4Ptfq6G0fPCwWysH2QATedGI'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
FILENAME = 'document.txt'

# Run through the OAuth flow and retrieve credentials

# Check for existing credentials

config_path = os.path.expandvars('$HOME/.config/pygdrived/config')
config_exists = os.path.exists(config_path)

#flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
#print(dir(flow))
#authorize_url = flow.step1_get_authorize_url()

'''
if not config_exists:
    webbrowser.open(authorize_url)
    #print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()

    credentials = flow.step2_exchange(code)

    head, tail = os.path.split(config_path)

    try:
        os.makedirs(head)
    except:
        pass

    fd = open(config_path, 'w')
    http = httplib2.Http()
    http = credentials.authorize(http)

    pickle.dump(http, fd, pickle.HIGHEST_PROTOCOL)
else:
    fd = open(config_path, 'r')
    http = pickle.load(fd)
'''
# Create an httplib2.Http object and authorize it with our credentials

#drive_service = build('drive', 'v2', http=http)

# Insert a file
#media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
body = {
  'title': 'My document',
  'description': 'A test document',
  'mimeType': 'text/plain'
}

#file = drive_service.files().insert(body=body, media_body=media_body).execute()
#pprint.pprint(file)


def main(args):
    return

