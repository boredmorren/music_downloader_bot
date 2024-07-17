from yandex_music import Client
import os

client = Client(os.getenv('YANDEX_TOKEN')).init()


def print_all_tracks(query):
    track_list = search_tracks(query)
    track_dict = {}

    for i, track in enumerate(track_list, 1):
        if i <= 10:
            track_dict[track] = track.artists[0].name  + ' - ' + track.title
    
    return track_dict
   
def download_track(track):
    track_filename = track.title + '.mp3'
    client.tracks(str(track.id) + ':' + str(track.albums[0]["id"]))[0].download(track.title + ".mp3")
    return track_filename

def search_tracks(query):

    search_result = client.search(query)

    return search_result.tracks.results