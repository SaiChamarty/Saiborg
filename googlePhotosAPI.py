
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import aiohttp

# Scopes/permissions needed for Google Photos API
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.appendonly']

creds = Credentials.from_authorized_user_file('token.json', SCOPES)

def list_albums(service):
    albums = service.albums().list(pageSize=10).execute()
    return albums.get('albums', [])

async def fetch_and_list_albums():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    albums = list_albums(service)
    for album in albums:
        print(f"Album ID: {album['id']}, Album Title: {album['title']}")

# Function to create Google Photos service
def create_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

# Create an album and return its ID
def create_album(album_title):
    service = create_service()

    # Step 1: List all albums and search for the album title
    albums = service.albums().list(pageSize=50).execute()
    existing_albums = albums.get('albums', [])

    for album in existing_albums:
        if album['title'].lower() == album_title.lower():
            print(f"Album '{album_title}' already exists.")
            return album['id']  # Return the existing album ID

    # Step 2: If album doesn't exist, create a new one
    print(f"Album '{album_title}' does not exist, creating a new album.")
    request_body = {'album': {'title': album_title}}
    album = service.albums().create(body=request_body).execute()

    return album['id']  # Return the new album ID

# Upload image to Google Photos
async def upload_to_google_photos(image_data, filename, album_id):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

    # Step 1: Upload the image to Google Photos
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': filename,
        'X-Goog-Upload-Protocol': 'raw',
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(upload_url, headers=headers, data=image_data) as response:
            if response.status == 200:
                upload_token = await response.text()
            else:
                raise Exception(f"Failed to upload image: {response.status}")

    # Step 2: Create a media item with the upload token
    media_item = {
        "newMediaItems": [
            {
                "simpleMediaItem": {
                    "uploadToken": upload_token
                }
            }
        ]
    }
    response = service.mediaItems().batchCreate(body=media_item).execute()
    media_item_id = response['newMediaItemResults'][0]['mediaItem']['id']

    # Step 3: Add media item to album
    service.albums().batchAddMediaItems(
        albumId=album_id,
        body={
            "mediaItemIds": [
                media_item_id
            ]
        }
    ).execute()

# Download image
async def download_image(image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            if resp.status == 200:
                return await resp.read()
    return None

# Download and upload image
async def download_and_upload_to_google_photos(image_url, album_title):
    image_data = await download_image(image_url)
    if image_data:
        album_id = create_album(album_title)  # Create album and get ID
        await upload_to_google_photos(image_data, 'uploaded_image', album_id)
