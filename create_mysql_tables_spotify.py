#!/usr/bin/env python
# coding: utf-8

# In[3]:


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import *
import re


###


# read credentials from mysql_credentials.txt
mysql_credentials = {}

with open("mysql_credentials.txt") as doc:
    for line in doc:
        (key, val) = line.split()
        mysql_credentials[str(key)] = val # create mysql credentials dict

mysql_key = list(mysql_credentials.values()) # create mysql credential list for *args


# read credentials from spotify_credentials.txt
spotify_credentials = {}

with open("spotify_credentials.txt") as doc:
    for line in doc:
        (key, val) = line.split()
        spotify_credentials[str(key)] = val # create spotify credentials dict for **kwargs


# read playlist ids from playlist_urls.txt
playlist_urls = open("playlist_urls.txt", "r").read().splitlines()
playlist_ids = []

for i in range(0,len(playlist_urls)):
    playlist_ids.append(re.split('/|\:', playlist_urls[i])[-1]) # strip id off end of url

    
###


# establish spotify client credentials
client_credentials_manager = SpotifyClientCredentials(**spotify_credentials) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

tracklist_dict = {}

for i in range(0,len(playlist_urls)):
    tracklist_dict.update(sp.playlist(playlist_ids[i]))
    
tracklist = pd.DataFrame()

for i in range(0, tracklist_dict['tracks']['total']):
    tracklist_info = []
    for field in list(tracklist_dict['tracks']['items'][0]['track'].keys()):
        tracklist_info.append(tracklist_dict['tracks']['items'][i]['track'][field])
    tracklist = tracklist.append([tracklist_info], ignore_index=True)
    
tracklist.columns = list(tracklist_dict['tracks']['items'][0]['track'].keys())

###


# table schema

track_fields = {'track_id' : 'varchar(22)',
                 'artist_id' : 'varchar(22)',
                 'album_id' : 'varchar(22)',
                 'duration' : 'int', # in ms
                 'track_popularity' : 'int',
                 'playlist_id' : 'varchar(22)'}

artist_fields = {'artist_id' : 'varchar(22)',
                 'artist_name' : 'varchar()',
                 'artist_followers' : 'int',
                 'artist_popularity' : 'int'}

album_fields = {'album_id' : 'varchar(22)',
                 'album_name' : 'varchar()',
                 'artist_id' : 'varchar(22)',
                 'album_popularity' : 'int',
                 'record_label' : 'varchar()',
                 'track_count' : 'int',}

playlist_fields = {'playlist_id' : 'varchar(22)',
                 'playlist_name' : 'varchar()',
                 'playlist_followers' : 'int',
                 'track_list' : 'varchar()',  # list of strings
                 'track_count' : 'int'}

# create empty datafraames for each table

track_df = pd.DataFrame(columns = list(track_fields.keys()))
artist_df = pd.DataFrame(columns = list(artist_fields.keys()))
album_df = pd.DataFrame(columns = list(album_fields.keys()))
playlist_df = pd.DataFrame(columns = list(playlist_fields.keys()))


###


# populate dataframes

track_df['track_id'] = tracklist['id']

artist_ids = []
artist_names = []
album_ids = []
album_names = []

for i in range(0,len(track_df)):
    
    artist_ids.append(tracklist['artists'][i][0]['id'])
    artist_names.append(tracklist['artists'][i][0]['name'])
    
    album_ids.append(tracklist['album'][i]['id'])
    album_names.append(tracklist['album'][i]['name'])

track_df['artist_id'] = artist_ids
track_df['album_id'] = album_ids
track_df['duration'] = tracklist['duration_ms']
track_df['track_popularity'] = tracklist['popularity']

artist_df['artist_id'] = artist_ids
artist_df['artist_name'] = artist_names

album_df['album_id'] = album_ids
album_df['artist_id'] = artist_ids
album_df['album_name'] = album_names


artist_followers = []
artist_popularity = []

for i in artist_df['artist_id']:
    artist_info = sp.artist(i)
    artist_followers.append(artist_info['followers']['total'])
    artist_popularity.append(artist_info['popularity'])
    
artist_df['artist_followers'] = artist_followers
artist_df['artist_popularity'] = artist_popularity


album_popularity = []
record_label = []
release_date = []
track_count = []

for i in album_df['album_id']:
    album_info = sp.album(i)
    album_popularity.append(album_info['popularity'])
    record_label.append(album_info['label'])
    release_date.append(album_info['release_date'])
    track_count.append(album_info['total_tracks'])
    
album_df['album_popularity'] = album_popularity
album_df['record_label'] = record_label
album_df['release_date'] = release_date
album_df['track_count'] = track_count

###


# open mysql connection
engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(*mysql_key))

# create track table
track_df.to_sql('track', con=engine)

# create artist table
artist_df.to_sql('artist', con=engine)

# create album table
album_df.to_sql('album', con=engine)

# close mysql connection
engine.dispose()


# In[ ]:




