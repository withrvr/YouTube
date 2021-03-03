from config_api import youtube  # , save_as_json
import re
import datetime

# to calculate the total time
total_vid_duration = datetime.timedelta()

# pattern to serch hh mm ss in the duration
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

# enter the playlist id to search or ('PLaAkIIUdfDM4DEgB4Djmp5_E2mXZlEEYM')
playlistId = input("Enter Playlist ID :- ")
nextPageToken = None

# nextPageToken, as maxResults at a time is 50 only.... then next, then next
while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlistId,
        # playlistId='PLaAkIIUdfDM4DEgB4Djmp5_E2mXZlEEYM',
        maxResults=50,
        pageToken=nextPageToken,
    )
    pl_response = pl_request.execute()

    # getting all the ids of the video in the playlist
    vid_ids = [
        item["contentDetails"]["videoId"]
        for item in pl_response['items']
    ]

    vid_request = youtube.videos().list(
        part='contentDetails',
        id=",".join(vid_ids),
    )
    vid_responce = vid_request.execute()
    # save_as_json(vid_responce, 'foo')

    # looping over all the videos in the playlist
    for item in vid_responce['items']:
        duration = item["contentDetails"]["duration"]

        # searching in the duration for hours minutes and seconds
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        # converting it into int
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        # making timdelta obj
        vid_duration = datetime.timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )

        print(vid_duration)
        total_vid_duration += vid_duration

    print("fetching... next videos...")
    print(f"till Now Total duration is :- {total_vid_duration}")

    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break


# login to convert seconds to .. hh mm ss
s = int(total_vid_duration.total_seconds())
hours, remainder = divmod(s, 3600)
minutes, seconds = divmod(remainder, 60)

print()
print(
    f"\nFinal Total duration of Playlist is \n--> {hours} hrs {minutes} min {seconds} sec <--"
)
print()
