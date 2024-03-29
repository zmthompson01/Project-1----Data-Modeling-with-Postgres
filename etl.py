import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import create_tables

def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files

def process_song_file(cur, filepath):
    # open song file
    df = pd.DataFrame.from_dict(pd.read_json(get_files(filepath='data/song_data')[0], typ='series')).T

        
    # create song table and insert song record
    cur.execute(song_table_create)
    song_data = list(df[['title', 'song_id', 'artist_id', 'year', 'duration']].iloc[0,:])
    cur.execute(song_table_insert, song_data)

    
    # create artist table and insert artist record
    cur.execute(artist_table_create)
    artist_data = list(df[['artist_id','artist_name','artist_latitude', 'artist_longitude']].iloc[0,:])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.concat([pd.DataFrame.from_dict(pd.read_json(i, lines=True)) for i in get_files(filepath='data/log_data')])

    
    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
    
    
    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    
    # insert time data records
    time_df = pd.DataFrame({
        'ts':df['ts']
        ,'hour':df['ts'].dt.hour
        ,'day':df['ts'].dt.day
        ,'week':df['ts'].dt.week
        ,'month':df['ts'].dt.month
        ,'year':df['ts'].dt.year
        ,'weekday':df['ts'].dt.weekday})

    
    # create time table and  inster time row
    cur.execute(time_table_create)
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

        
    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    
    # create user table and insert user record
    cur.execute(user_table_create)
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

        
    #create songplay table and insert songplay records
    cur.execute(songplay_table_create)
    for index, row in df.iterrows():
        
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

            
    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    
    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # create database `sparkifydb`
    create_tables.create_database()
    
    
    # connect to database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    
    # run dimension table creations
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)

    
    # run fact table creation
    process_data(cur, conn, filepat h='data/log_data', func=process_log_file)

    conn.close()


# run etl    
if __name__ == "__main__":
    main()