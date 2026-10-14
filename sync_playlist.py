import os
import csv
from googleapiclient.discovery import build

API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST_ID = 'PLH7gF6djms2jG6tyfnDs8Sve8p3_BwC5I' # e.g., PL...

def get_playlist_items(youtube, playlist_id):
    items = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            snippet = item['snippet']
            items.append({
                'Title': snippet['title'],
                'Video ID': snippet['resourceId']['videoId'],
                'Channel': snippet['videoOwnerChannelTitle'] if 'videoOwnerChannelTitle' in snippet else 'Unknown',
                'Added At': snippet['publishedAt']
            })
            
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
            
    return items

if __name__ == '__main__':
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    videos = get_playlist_items(youtube, PLAYLIST_ID)
    
    # Write to CSV
    with open('playlist_export.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['Title', 'Video ID', 'Channel', 'Added At'])
        writer.writeheader()
        writer.writerows(videos)
        
    print(f"Successfully exported {len(videos)} songs.")