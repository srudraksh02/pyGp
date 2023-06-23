import pickle 
import requests 	#to send HTTP requests
import os
from Google import Create_Service

API_NAME='photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = 'googlePhotos.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

image_dir = os.path.join(os.getcwd(),' DIRECTORY_NAME ')
upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
token = pickle.load(open('token_photoslibrary_v1.pickle','rb'))		#reads the pickled version of data and loads it as the data hierarchy

headers = {
	'Authorization': 'Bearer ' + token.token,		#to grant access to the photos server
	'Content-type': 'application/octet-stream',		#to indicate the media type of the resource
	'X-Goog-Upload-Protocol': 'raw',
}


image_file = os.path.join(image_dir,'cat1.jpeg')
headers['X-Goog-Upload-File-Name'] = 'name_test2.jpg'

img = open(image_file,'rb').read()
response = requests.post(upload_url,data=img,headers=headers)
request_body  = {
	'newMediaItems':[
		{
		'description': 'this is a test',
		'simpleMediaItem' : {
			'uploadToken' : response.content.decode('utf-8')
			}
		}
	]
}

upload_response = service.mediaItems().batchCreate(body=request_body).execute()