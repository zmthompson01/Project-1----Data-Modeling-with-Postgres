# DROP TABLES

songplay_table_drop = "DROP TABLE songplay"
user_table_drop = "DROP TABLE users"
song_table_drop = "DROP TABLE songs"
artist_table_drop = "DROP TABLE artists"
time_table_drop = "DROP TABLE time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay (
        ts TIMESTAMP
        ,userId INT
        ,level VARCHAR(10)
        ,song_id VARCHAR(50)
        ,artist_id VARCHAR(50)
        ,sessionId INT
        ,location VARCHAR(500)
        ,userAgent VARCHAR(500)
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        userId INT
        ,firstName VARCHAR(50)
        ,lastName VARCHAR(50)
        ,gender CHAR
        ,level VARCHAR(10)
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        title VARCHAR(100)
        ,song_id VARCHAR(50)
        ,artist_id VARCHAR(50)
        ,year INT
        ,song_length NUMERIC(16,4)
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR(50)
        ,artist_name VARCHAR(50)
        ,artist_latitude NUMERIC(38,10)
        ,artist_longitude NUMERIC(38,10)
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        ts TIMESTAMP
        ,hour INT
        ,day INT
        ,week INT
        ,month INT
        ,year INT
        ,weekday INT
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplay VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    INSERT INTO users VALUES (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
    INSERT INTO songs VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
    INSERT INTO artists VALUES (%s, %s, %s, %s)
""")

time_table_insert = ("""
    INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
    SELECT
        s.song_id
        ,a.artist_id
    FROM
        (SELECT artist_id, artist_name FROM artists WHERE artist_name = %s) a
        JOIN (SELECT song_id, artist_id FROM songs WHERE title = %s AND song_length = %s) s
            ON a.artist_id = s.artist_id
    ;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]