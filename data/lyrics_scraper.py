"""
Simple web scraper to find lyrics for given songs

Every API I've found to do this has been complete suckage, so
I'm just going to manually scrape the song lyrics from:
metrolyrics.com

I may consider other sites if the success rate on metrolyrics is low.
"""

import settings

class LyricsScraper(object):
    """ Class to encapsulate functionality of scraping lyrics """
    def __init__(song_title, song_artist):
        self.song_title = song_title
        self.song_artist = song_artist

    def load_song_html(self):
        """ Load the html for the song """
        # TODO: Use a python scraper module to get the html for the song lyrics page
        # one metrolyrics, the page url is: www.metrolyrics.com/song-name-lyrics-artist.html
        # If the song doesn't exist but the artist does, this redirects to the artist page.
        # If the song and the artist don't exist, this gives a 404
        # If the lyrics page is correctly loaded, the div wrapping the lyrics has id='lyrics-body-text'
        # The song is split in to verses, each a p tag with class='verse'
        pass

    def get_lyrics(self):
        """
        Returns the lyrics for the song the scraper was made for.

        Must be called after load_song_html
        """
        pass

def load_songs():
    """ Load the list of songs/artist names to grab lyrics for """
    return [{'title': 'example', 'artist': 'example'}]

def save_lyrics(songs):
    """ Saves lyrics for all given songs to the results file """
    for song in songs:
        lyrics = get_lyrics(song)
        # Now write out lyrics to result...

def get_lyrics(song):
    """ Get lyrics for the given song """
    scraper = LyricsScraper(song['title'], song['artist'])
    scraper.load_song_html() # Raise exception to detect error?
    lyrics = scraper.get_lyrics()
    return lyrics

if __name__ == '__main__':
    songs = load_songs()
    save_lyrics(songs)
