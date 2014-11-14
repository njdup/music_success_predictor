"""
Implements a simple baseline classifier of music success
"""

import json
from sklearn import linear_model
import numpy as np

if __name__ == '__main__':
    song_info = {}
    with open('data/inputs/data.json', 'r') as data:
        song_info = json.load(data)

    songs = song_info['song_data']
    half = len(songs)/2
    songs_train = songs[:half]
    songs_test = songs[half+1:]

    # prepare the data to pass into the linear regression learner
    song_x_train = []
    song_y_train = []

    artists = {} # Map artist names to the their index in the feature vector
    index = 0
    x_inputs = []

    # Prepare the x input array based on artists
    for song in songs:
        artist = song[1]['artist']
        if artist in artists: continue
        x_inputs.append(0)
        artists[artist] = index
        index += 1

    for song in songs_train:
        feature_vector = [0]*len(x_inputs)
        artist = song[1]['artist']
        feature_vector[artists[artist]] = 1
        song_x_train.append(feature_vector)
        song_y_train.append(song[2]) # Map to hotttnesss score

    print song_y_train

    linear_reg = linear_model.LinearRegression()
    linear_reg.fit(np.array(song_x_train), np.array(song_y_train))

    print 'Coefficients: \n {}'.format(linear_reg.coef_)

    song_x_test = []
    song_y_test = []
    for song in songs_test:
        feature_vector = [0]*len(x_inputs)
        artist = song[1]['artist']
        feature_vector[artists[artist]] = 1
        song_x_test.append(feature_vector)
        song_y_test.append(song[2])

    score = linear_reg.score(np.array(song_x_test), np.array(song_y_test))
    print 'Score: {}'.format(score)
