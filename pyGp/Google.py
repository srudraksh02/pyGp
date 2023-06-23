#REST is a software architecture that imposes conditions on how an API should work
#SERVICE: it is a software that performs automated tasks
#OAuth: When an app or a resource wants to access resources from another web app on behalf of another user
#CLIENT_SECRET_FILE: Contains all the info needed to interact with an OAuth 2.0 protected file
#SCOPES: Enables you to group a set a REST resources and methods for an API
#TOKEN: allows a user to authenticate with cloud apps na dretrieve data from the instance through REST APIs

#   --------------------------------------------------------------------------------------------------

import pickle       #to serialize objects
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow      #to run the OAuth2.0 Authorization Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload    #to manage media file uploads
from google.auth.transport.requests import Request      #transport adapter for requests

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'      #creates the token file (.pickle file)
    print(pickle_file)

    if os.path.exists(pickle_file):         #checks if the path specified exists or not 
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)       #.load is used to load pickled data from a file like object

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)    #to perform the application authorization flow. 
            cred = flow.run_local_server()  #prints a message to instruct the user to open a URL

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)        #.dump() used to store the data to a file. Storing the cred object in cred file

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred, static_discovery=False)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
       print('Unable to connect.')
       print(e)
       return None