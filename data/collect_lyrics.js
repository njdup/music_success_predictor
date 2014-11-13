// Module for collecting and saving song lyrics
// Draws the list of songs and artist names from an expected stored file

var rapgeniusClient = require('rapgenius-js');

var settings = require('./settings');
var songsList = require(settings.songsPath);

var getSongLyrics = function(){
  //for (song in songsList.songs){
    song = songsList.songs[4]
    console.log(song)
    rapgeniusClient.searchSong(song.song_name + ' by ' + song.artist, song.genre, function(err, songs){
      if(err){
        console.log("Error: " + err);
      } else {
        for (song in songs){
          console.log("Song: " + songs[song].name);
        }
      }
    });
  //}
}

getSongLyrics()
