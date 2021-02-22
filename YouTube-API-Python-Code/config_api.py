from googleapiclient.discovery import build
import api_keys
print()


# convert api responce obj to json object
def save_as_json(obj, fileName):
    import json
    # saving to the foo.json file
    with open(fileName + ".json", 'w') as file:
        json.dump(obj, file, indent=4)


# add your own api_key of yt here
api_key = api_keys.api_key_value
youtube = build('youtube', 'v3', developerKey=api_key)

# pl_request = youtube.playlistItems().list(
#     part='contentDetails',
#     playlistId=playlistId,
#     # playlistId='PLaAkIIUdfDM4DEgB4Djmp5_E2mXZlEEYM',
#     maxResults=50,
#     pageToken=nextPageToken,
# )
# pl_response = pl_request.execute()
