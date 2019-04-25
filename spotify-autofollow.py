import requests
import json

api_token = '<API_TOKEN>'
api_url_base = 'https://api.spotify.com/v1'
api_url_get_saved_tracks = '/me/tracks?market=US&'
api_url_follow_artists = '/me/following?type=artist'

headers = {'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(api_token)}

def main():
    print('Hello world!')
    artist_ids = get_artist_id_list()
    follow_artist_by_ids(artist_ids)

# Retrieve list of unique saved tracks.
# offset: starting point
# limit: max 50
def get_saved_tracks(offset=0, limit=0, next_url=None):
    response = requests.get(str(next_url) if next_url is not None else api_url_base + api_url_get_saved_tracks + "offset=" + str(offset) + "&limit=" + str(limit), headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

# Get list of unique artist_ids
def get_artist_id_list():
    artist_ids = []

    saved_tracks = get_saved_tracks(offset=0, limit=50)
    
    if saved_tracks is not None:
        while True:
            for item in saved_tracks['items']:
                if not item['track']['artists'][0]['id'] in artist_ids:
                    artist_ids.append(item['track']['artists'][0]['id'])
                    print(item['track']['artists'][0]['id'])
            if saved_tracks['next'] is None:
                break
            saved_tracks = get_saved_tracks(next_url=saved_tracks['next'])
            
    else:
        print("There was a problem retrieving saved tracks...")

    return artist_ids

def follow_artist_by_ids(artist_ids):
    for artist_id_group in chunker(artist_ids, 50):
            response = requests.put(api_url_base + api_url_follow_artists + "&ids=" + "%2C".join(artist_id_group), headers=headers)
            print(response.status_code)


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

if __name__ == "__main__": main()
