"""
Simple web scraper to find lyrics for given songs

Every API I've found to do this has been complete suckage, so
I'm just going to manually scrape the song lyrics from:
metrolyrics.com

I may consider other sites if the success rate on metrolyrics is low.
"""

import settings
import string
import json

from bs4 import BeautifulSoup, NavigableString
from urllib2 import urlopen

class LyricsScraper(object):
    """ Class to encapsulate functionality of scraping lyrics """
    def __init__(self, song_title, song_artist):
        self.song_title = song_title.replace(' ', '-')
        self.song_artist = song_artist.replace(' ', '-')
        self.lyrics = None

    def load_song_html(self):
        """ Load the html for the song """
        # TODO: Use a python scraper module to get the html for the song lyrics page
        # one metrolyrics, the page url is: www.metrolyrics.com/song-name-lyrics-artist.html
        # If the song doesn't exist but the artist does, this redirects to the artist page.
        # If the song and the artist don't exist, this gives a 404
        # If the lyrics page is correctly loaded, the div wrapping the lyrics has id='lyrics-body-text'
        # The song is split in to verses, each a p tag with class='verse'
        lyrics_url = settings.METROLYRICS_BASE + '/' + self.song_title + '-lyrics-' + self.song_artist + '.html'
        html = urlopen(lyrics_url).read()
        soup = BeautifulSoup(html)
        lyrics_section = soup.find(id=settings.LYRICS_SECTION)
        self.lyrics = lyrics_section

    def get_lyrics(self):
        """
        Returns the lyrics for the song the scraper was made for.

        Must be called after load_song_html
        """
        if not self.lyrics: raise Exception('Must load html first!')

        result = []
        for verse in self.lyrics.findAll('p'):
            verse = self.to_string_strip_tags(verse)
            punctuation = set(string.punctuation)
            verse = ''.join(ch for ch in verse if ch not in punctuation)
            result.append(verse)

        return result

    def to_string_strip_tags(self, tag):
        """
        Strips html tags from given tag object and returns it as a string
        """
        replace = ''
        for content in tag.contents:
            if not isinstance(content, NavigableString):
                content = self.to_string_strip_tags(content)
            replace += unicode(content)
        return replace

def load_songs():
    """ Load the list of songs/artist names to grab lyrics for """
    #return [{'title': 'chum', 'artist': 'earl sweatshirt'}]
    result = []
    with open(settings.SONGNAMES_FILE, 'r') as song_data:
        songs = json.load(song_data)
        songs = songs['songs']
        result = [{'title': song['song_name'], 'artist': song['artist']} for song in songs]
    return result

def save_lyrics(songs):
    """ Saves lyrics for all given songs to the results file """
    with open(settings.LYRICS_FILE, 'w') as outfile:
        outfile.write('{ "lyrics": [ \n')
        for index, song in enumerate(songs):
            lyrics = '\n'.join(get_lyrics(song))
            outfile.write(json.dumps({' '.join([song['title'], song['artist']]): lyrics}))
            if index != len(songs)-1:
                outfile.write(',\n')
        outfile.write('] }')

def get_lyrics(song):
    """ Get lyrics for the given song """
    scraper = LyricsScraper(song['title'], song['artist'])
    scraper.load_song_html() # Raise exception to detect error?
    lyrics = scraper.get_lyrics()
    return lyrics

if __name__ == '__main__':
    songs = load_songs()
    save_lyrics(songs)
