from config_api import youtube, save_as_json

# enter the playlist id to search ('PLaAkIIUdfDM4DEgB4Djmp5_E2mXZlEEYM')
playlistId = input(
    "Enter Playlist ID :- ") or 'PLaAkIIUdfDM4DEgB4Djmp5_E2mXZlEEYM'
nextPageToken = None

videos = []

# nextPageToken, as maxResults at a time is 50 only.... then next, then next
while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlistId,
        maxResults=50,
        pageToken=nextPageToken,
    )
    pl_response = pl_request.execute()

    # getting all the ids of the video in the playlist
    vid_ids = [
        item["contentDetails"]["videoId"]
        for item in pl_response['items']
    ]

    # video request and responce
    vid_request = youtube.videos().list(
        part='statistics',
        id=",".join(vid_ids),
    )
    vid_responce = vid_request.execute()
    save_as_json(vid_responce, 'foo')

    # looping over all the videos in the playlist

    videos += [
        {
            'view': int(item['statistics']['viewCount']),
            'like': int(item['statistics']['likeCount']),
            'dislike': int(item['statistics']['dislikeCount']),
            'comment': int(item['statistics']['commentCount']),
            'url': f'https://youtu.be/{item["id"]}/',
        }
        for item in vid_responce['items']
    ]

    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break


# filter your video here
sort_by = input("Sort By (view, like, dislike, comment):- ")
if sort_by not in ("view", "like", "dislike", "comment"):
    print(f"sort by is selected ... because {sort_by} is not the properone")
    sort_by = 'view'

top_limit = int(input("enter the limit (top ??) :- "))
if (top_limit < 1):
    print(f"top_limit = 3 is selected ..because {top_limit} is not properone")
    top_limit = 3

most_popular = True

# sorting the video
videos.sort(key=lambda video: video[sort_by], reverse=most_popular)

# looping the videos
print()
for video in videos[:top_limit]:
    print(f"{video['url']} ... {sort_by} -> {video[sort_by]}")
