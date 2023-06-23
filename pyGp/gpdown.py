import os
from Google import Create_Service
import pandas as pd  
import requests

pd.set_option('display.max_columns',100)
pd.set_option('display.max_rows',150)
pd.set_option('display.max_colwidth',150)
pd.set_option('display.width',120)
pd.set_option('expand_frame_repr',True)

API_NAME='photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = 'googlePhotos.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

destination_folder = ' PATH OF DESTINATION FOLDER '

myAlbums = service.albums().list().execute()		#gets the URLs of all the albums 

myAlbums_list = myAlbums.get('albums')
dfAlbums = pd.DataFrame(myAlbums_list)

#print(dfAlbums)

C_id = dfAlbums[dfAlbums['title'] == 'INSERT_NAME_OF_ALBUM ']['id'].to_string(index=False).strip()
print(C_id,'\n')


def download_file(url:str,destination_folder:str,file_name:str):
	response = requests.get(url)
	if response.status_code == 200:
		print('Downloading file {0}'.format(file_name))
		with open(os.path.join(destination_folder,file_name),'wb') as f:
			f.write(response.content)
			f.close()

media_files = service.mediaItems().search(body={'albumId': C_id}).execute()['mediaItems']

for media_file in media_files:
	file_name = media_file['filename']
	download_url = media_file['baseUrl'] + '=d'
	download_file(download_url,destination_folder,file_name)

print("Done downloading the files!")