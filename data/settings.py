"""
Various settings for music data collecting
"""

MUSIC_INFO_API = 'http://developer.echonest.com/api/v4/song/search'
API_KEY = '0AUAGZNQLKRLAILXK'

LYRICS_API = 'http://api.musixmatch.com/ws/1.1/track.lyrics.get'
LYRICS_API_KEY = 'ce40d0b7a1bf18d71cf8e006d2a8a8b7'

GENRES = [
    'rap',
    'rock',
    'country',
    'hip hop',
    'indie rock',
    'pop',
    'r&b'
]

POPULARITY_RANGES = {
    'POPULAR': '0.8',
    'UPPER_MEDIOCRE': '0.79',
    'LOWER_MEDIOCRE': '0.4',
    'UNPOPULAR': '0.39'
}

NUM_SONGS = 100

# Better to use python os.path functionality here, but oh well
SONGNAMES_FILE = 'songs/song_names.json'
LYRICS_SCRIPT = 'collect_lyrics.js'
LYRICS_FILE = 'lyrics/all.json'
