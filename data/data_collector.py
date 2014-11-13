"""
Simple script to collect a list of popular/unpopular songs,
and metadata and lyrics for each song.
"""

import requests
import settings
import json
from subprocess import call

SONGNAME_INDEX = 0
ARTIST_INDEX = 1
GENRE_INDEX = 2

def get_popular_song_names(genre):
    """ Returns a list of current popular songs """
    songs = set()

    data = {
        'api_key': settings.API_KEY,
        'results': settings.NUM_SONGS,
        'style': genre
    }
    response = requests.get(settings.MUSIC_INFO_API, params=data).json()
    data = response['response']
    for song in data['songs']:
        songs.add((song['title'], song['artist_name'], genre))

    return songs

def convert_to_dict(song):
    result = {
        "song_name": song[SONGNAME_INDEX],
        "artist": song[ARTIST_INDEX],
        "genre": song[GENRE_INDEX],
    }
    return result

def write_out_song_info(songs):
    with open(settings.SONGNAMES_FILE, 'w') as f:
        f.write('{"songs": [ ')
        #for song in songs:
        for index, song in enumerate(songs):
            song = convert_to_dict(song)
            f.write(json.dumps(song))
            if index != len(songs) - 1:
                f.write(',\n')
        f.write("] }")

def collect_song_lyrics(songs):
    """
    Gathers and saves the lyrics for the given songs

    Uses the echo nest and musixmatch APIs in tandem to get query for the lyrics
    """
    with open(settings.LYRICS_FILE, 'w') as output:
        output.write('{ "lyrics": [ \n')
        for index, song in enumerate(songs):
            data = {
                'api_key': settings.API_KEY,
                'format': 'json',
                'artist': song[ARTIST_INDEX],
                'title': song[SONGNAME_INDEX],
                'bucket': 'id:musixmatch-WW'
            }

            try:
                # This is some janky shit right here
                get_foreign_key = requests.get(settings.MUSIC_INFO_API, params=data, timeout=10).json()
            except:
                print 'Error occurred'

            if 'songs' not in get_foreign_key['response']:
                continue
            foreign_ids = get_foreign_key['response']['songs'][0]['foreign_ids']
            if not foreign_ids: continue
            musixMatch_id = foreign_ids[0]['foreign_id'].split(':')[2]

            print 'Retrieving lyrics for {song}'.format(song=song[SONGNAME_INDEX].encode('utf-8'))
            try:
                musix_response = requests.get(
                    settings.LYRICS_API,
                    params={
                        'apikey': settings.LYRICS_API_KEY,
                        'track_id': musixMatch_id
                    },
                    timeout=10
                ).json()
            except:
                print 'Error occurred'

            lyrics = musix_response['message']['body']['lyrics']['lyrics_body']
            # Get rid of their stupid disclaimer.
            lyrics = lyrics.replace('******* This Lyrics is NOT for Commercial use *******', '')

            # Write to the json output file, mapping 'song_name artist_name': lyrics
            output.write(json.dumps({song[SONGNAME_INDEX] + song[ARTIST_INDEX]: lyrics}))
            if index != len(songs) - 1:
                output.write(',\n')
        output.write('] }')

if __name__ == '__main__':

    # First collect a list of songs + song names
    songs = set()
    print 'Collecting song and artists names from the following genres:'
    print settings.GENRES

    for genre in settings.GENRES:
        songs = songs.union(get_popular_song_names(genre))

    print '{} songs collected'.format(len(songs))
    write_out_song_info(songs)

    print '\nCollecting song lyrics...'
    collect_song_lyrics(songs)
    print 'Done'

    #write_out_song_info(songs)
