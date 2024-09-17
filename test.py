from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/photoslibrary', 'https://www.googleapis.com/auth/photoslibrary.appendonly']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)

service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

# Test request to list albums
results = service.albums().list().execute()
albums = results.get('albums', [])

for album in albums:
    print(album['title'])

# async def download_image(image_url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(image_url) as resp:
#             if resp.status == 200:
#                 return await resp.read()
#     return None

# async def upload_to_google_photos(image_data, filename):
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

#     # Step 1: Upload the image to Google Photos
#     upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
#     headers = {
#         'Authorization': f'Bearer {creds.token}',
#         'Content-Type': 'application/octet-stream',
#         'X-Goog-Upload-File-Name': filename,
#         'X-Goog-Upload-Protocol': 'raw',
#     }

#     async with aiohttp.ClientSession() as session:
#         async with session.post(upload_url, headers=headers, data=image_data) as response:
#             if response.status == 200:
#                 upload_token = await response.text()
#             else:
#                 raise Exception(f"Failed to upload image: {response.status}")

#     # Step 2: Create a media item with the upload token
#     media_item = {
#         "newMediaItems": [
#             {
#                 "simpleMediaItem": {
#                     "uploadToken": upload_token
#                 }
#             }
#         ]
#     }
#     album_id = 'AJ2a2NC499T2f7PwYITFGkBkDJce_nyfNU22dTgIzrC1D9InT7gZyUwb36lLIe5ujn0zaJPkKH_a'
#     service.mediaItems().batchCreate(body=media_item).execute()

#     # Step 3: Add media item to album
#     service.albums().batchAddMediaItems(
#         albumId=album_id,
#         body={
#             "mediaItemIds": [
#                 upload_token  # This should be the mediaItemId obtained from the previous step
#             ]
#         }
#     ).execute()



# # Function to upload image to Google Photos
# # async def upload_to_google_photos(image_data, filename):
# #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# #     service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)

# #     upload_token = service.mediaItems().upload(
# #         media_body=image_data,
# #         filename=filename,
# #     ).execute()

# #     # Add the uploaded image to a specific album (use your album ID)
# #     album_id = 'AF1QipOIizy83JS3g_NirzLOwhnmKTosgujMFhNwrWHM'
# #     media_item = {
# #         "newMediaItems": [
# #             {
# #                 "simpleMediaItem": {
# #                     "uploadToken": upload_token,
# #                 }
# #             }
# #         ]
# #     }
# #     service.albums().batchAddMediaItems(albumId=album_id, body=media_item).execute()

# async def download_and_upload_to_google_photos(image_url):
#     image_data = await download_image(image_url)
#     if image_data:
#         await upload_to_google_photos(image_data, 'uploaded_image.jpg')



# @client.event
# async def on_message(message):
#     # Ignore messages from the bot itself
#     if message.author == client.user:
#         return

#     # Check if the message is in the #pictures channel
#     if str(message.channel) == 'pictures':
#         # Check if there are attachments (images)
#         if message.attachments:
#             for attachment in message.attachments:
#                 if any(attachment.filename.lower().endswith(ext) for ext in ['jpg', 'jpeg', 'png', 'gif', '.heic', '.mov', '.mp4', '.avi']):
#                     # Download the image
#                     image_url = attachment.url
#                     await download_and_upload_to_google_photos(image_url)
#                     await message.channel.send("Image has been uploaded to the album!")

#     await client.process_commands(message)



# def authorize():
#     flow = InstalledAppFlow.from_client_secrets_file(
#         'credentials.json', SCOPES)
#     creds = flow.run_local_server(port=0)
#     with open('token.json', 'w') as token:
#         token.write(creds.to_json())

# authorize()
