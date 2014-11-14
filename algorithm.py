"""
Implements a more advanced regression model for classifying
"""

import json
from sklearn.linear_model import Lasso
import numpy as np

if __name__ == '__main__':
    song_info = {}
    with open('data/inputs/data.json', 'r') as data:
        song_info = json.load(data)

    songs = song_info['song_data']
    half = len(songs)/2
    songs_train = songs[:half]
    songs_test = songs[half+1:]

    artists = {} # Map artist names to the their index in the feature vector
    index = 0
    artist_inputs = []

    # Prepare the artist input array based on artists
    for song in songs:
        artist = song[1]['artist']
        if artist in artists: continue
        artist_inputs.append(0)
        artists[artist] = index
        index += 1

    song_x_train = []
    song_y_train = []
    for song in songs_train:
        feature_vector = [0]*len(artist_inputs)
        artist = song[1]['artist']
        feature_vector[artists[artist]] = 1

        feature_dict = song[1]
        for feature, value in feature_dict.iteritems():
            if feature != 'artist' and feature !='genre':
                feature_vector.append(value)

        song_x_train.append(feature_vector)
        song_y_train.append(song[2]) # Map to hotttnesss score


    lasso_model = Lasso(alpha=0.1)
    lasso_model.fit(np.array(song_x_train), np.array(song_y_train))
    print lasso_model.coef_

    song_x_test = []
    song_y_test = []
    for song in songs_test:
        feature_vector = [0]*len(artist_inputs)
        artist = song[1]['artist']
        feature_vector[artists[artist]] = 1

        feature_dict = song[1]
        for feature, value in feature_dict.iteritems():
            if feature != 'artist' and feature != 'genre':
                feature_vector.append(value)

        song_x_test.append(feature_vector)
        song_y_test.append(song[2])

    prediction = lasso_model.predict(song_x_test[0])
    print 'Prediction: {}'.format(prediction)
    print 'Actual: {}'.format(song_y_test[0])
    score = lasso_model.score(np.array(song_x_test), np.array(song_y_test))
    print 'Score: {}'.format(score)
