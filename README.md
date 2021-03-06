# Creating a MySQL schema for the Spotify API
Creates a schema of relational tables in a local MySQL database by aggregating data from the Spotify API.


## spotify_database_schema
This image displays a basic schema for the created tables.
![Schema](https://github.com/cisteele/creating_mysql_schema_spotify_api/blob/main/spotify_database_schema.jpeg?raw=true)


## mysql_credentials.txt
This text file contains the credentials to connect to a local mysql database.  Be sure to update the values in the right column (user, password, host, database) with your servers details.

mysql_user user

mysql_pw password

mysql_host host

mysql_db database


## spotify_credentials.txt
This text file contains the credentials to connect to a the Spotify API.  Be sure to update the values in the right column (cid, secret) with your Spotify developer details.

client_id cid

client_secret secret


## playlist_urls.txt
This text file contains the urls of all playlists to scrape for songs to add to the database.  By default the file contains two playlist urls, "Techno 2020" and "Deep House 2020".  Replace these with your preferred playlist urls.  The specific form of the beginning of the url is unimportant, but the url must end with ".../playlist/<playlist_id>" where <playlist_id> is a string of 22 characters.  


## create_mysql_table_spotify.py
This python script will read the three config text files, scrape the desired playlists from the spotify API, and create the "track", "artist", and "album" tables in the specified MySQL database.  An error will occur if there are any tables with those names in the database already. 

This python script requires spotipy, pymysql, and sqlalchemy.


## sql_exercises
A sample of some SQL queries run on the created database when the default playlists ("Techno 2020" and "Deep House 2020') are loaded.
