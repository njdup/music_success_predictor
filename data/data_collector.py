"""
Simple script to collect a list of popular/unpopular songs,
and metadata and lyrics for each song.
"""

import requests
import settings
import json
import time
import re
from subprocess import call
from pyechonest import song as SongAPI
from pyechonest import config
config.ECHO_NEST_API_KEY = settings.API_KEY

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
        # get rid of anything in parens () or brackets []
        title = re.sub(r'\[((\w\s)+)\]', '', song['title'])
        title = re.sub(r'\((\w+)\)', '', title)
        print title

        songs.add((title, song['artist_name'], genre))

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
        output.write('\n]\n }')

def collect_song_data(songs):

    with open(settings.INPUTS_FILE, 'w') as output:
        output.write('{ "song_data": [ \n')
        for index, song in enumerate(songs):
            try:
                song_results = SongAPI.search(artist=song[ARTIST_INDEX], title=song[SONGNAME_INDEX])
            except:
                # They're rate-limiting us. Fuck them, sleep for 60 seconds and try again
                print 'Time to sleep...'
                time.sleep(60)
                print 'I\'m awake!'
                song_results = SongAPI.search(artist=song[ARTIST_INDEX], title=song[SONGNAME_INDEX])

            if not song_results: continue
            song_info = song_results[0]

            try:
                audio_summary = song_info.get_audio_summary()
            except:
                print 'I\'m sleeping!'
                time.sleep(60)
                print 'I\'m awake!'
                audio_summary = song_info.get_audio_summary()

            features = {feature: audio_summary[feature] for feature in settings.SONG_FEATURES}

            features['genre'] = song[GENRE_INDEX]
            features['artist'] = song[ARTIST_INDEX]

            try:
                features['artist_familiarity'] = song_info.get_artist_familiarity()
            except:
                print 'I\'m sleeping!'
                time.sleep(60)
                print 'I\'m awake'
                features['artist_familiarity'] = song_info.get_artist_familiarity()

            try:
                features['artist_hotttnesss'] = song_info.get_artist_hotttnesss()
            except:
                print 'I\'m sleeping!'
                time.sleep(60)
                print 'I\'m awake'
                features['artist_hotttnesss'] = song_info.get_artist_hotttnesss()

            try:
                song_hotttnesss = song_info.get_song_hotttnesss()
            except:
                print 'I\'m sleeping!'
                time.sleep(60)
                print 'I\'m awake!'
                song_hotttnesss = song_info.get_song_hotttnesss()

            print 'Info for song {song}: \n\n features: {features} \n\n hotttnesss: {hotttnesss}'.format(
                song = song[SONGNAME_INDEX].encode('utf-8'),
                features = features,
                hotttnesss = song_hotttnesss
            )
            data = (song[SONGNAME_INDEX], features, song_hotttnesss)
            output.write(json.dumps(data))
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

    """
    print '\nCollecting song lyrics...'
    collect_song_lyrics(songs)
    print 'Done'
    """

    #collect_song_data(songs)

    #write_out_song_info(songs)
