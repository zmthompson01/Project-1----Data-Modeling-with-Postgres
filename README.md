- Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
- State and justify your database schema design and ETL pipeline.
- [Optional] Provide example queries and results for song play analysis.


# Sparkify -- Data Modeling with Postgres

The goal of this database is to create an analytical data framework to identify users' behaviors. Currently all data is stored in logs and is not easily accessible to our analytics team. Our goal is to process these JSON files that house the raw Sparkify data into a consumable format for downstream teams.

Our team has created an ETL pipeline to parse the log information into a star schema made (fact and dimension tables) that makes analyzing events simpler. The fact table, `songplays`, lets consumers get all the relevant information needed for simple aggregations, like `COUNT`s of users or agents. If one neededs to deep dive a particular user, artist, or song, they can join the appropriate table back to the fact table to get their information. For example, if we needed so `COUNT` the number of unique songs listened to by user name, we could do something like the following:

~~~~
SELECT
    u.first_name | u.last_name AS user_name
    ,COUNT(s.song_id)
FROM
    songplays s
    JOIN users u
        ON s.user_id = u.user_id
GROUP BY
    1
~~~~

# Data Structure

### Fact Table
    
    songplays - records in log data associated with song plays i.e. records with page NextSong
        songplay_id
        , start_time
        , user_id
        , level
        , song_id
        , artist_id
        , session_id
        , location
        , user_agent

### Dimension Tables

    users - users in the app
        user_id
        , first_name
        , last_name
        , gender
        , level
    
    songs - songs in music database
        song_id
        , title
        , artist_id
        , year
        , duration
    
    artists - artists in music database
        artist_id
        , name
        , location
        , latitude
        , longitude
    
    time - timestamps of records in songplays broken down into specific units
        start_time
        , hour
        , day
        , week
        , month
        , year
        , weekday
