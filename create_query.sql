CREATE DATABASE cricket_data;
USE cricket_data;

CREATE TABLE IF NOT EXISTS matches (
            start_date DATE,
            teams_type VARCHAR(255),
            match_type VARCHAR(255),
            gender VARCHAR(255),
            match_id VARCHAR(50) PRIMARY KEY,
            team_involved_one VARCHAR(255),
            team_involved_two VARCHAR(255)
        );
        
CREATE TABLE IF NOT EXISTS meta_info (
match_id VARCHAR(255) PRIMARY KEY,
data_version VARCHAR(255),
created VARCHAR(255),
revision VARCHAR(255)
);
        
CREATE TABLE IF NOT EXISTS info_section (
match_id VARCHAR(255) PRIMARY KEY,
balls_per_over INT,
bowl_out VARCHAR(255),
city VARCHAR(255),
dates TEXT,
event TEXT,
gender VARCHAR(255),
match_type VARCHAR(255),
match_type_number INT,
missing VARCHAR(255),
officials TEXT,
outcome TEXT,
overs INT,
player_of_match TEXT,
players TEXT,
registry TEXT,
season TEXT,
supersubs VARCHAR(255),
team_type VARCHAR(255),
teams TEXT,
toss TEXT,
venue VARCHAR(255)
);

CREATE TABLE innings_info (
  match_id VARCHAR(255),
  team VARCHAR(255),
  declared VARCHAR(255),
  forfeited VARCHAR(255),
  powerplays TEXT,
  target TEXT,
  super_over TEXT,
  innings INT
);

CREATE TABLE over_section (
    match_id VARCHAR(255),
    innings VARCHAR(255),
    overs VARCHAR(10),
    batter VARCHAR(255),
    bowler VARCHAR(255),
    extras JSON,
    non_striker VARCHAR(255),
    review JSON,
    runs JSON,
    wickets JSON,
    replacements JSON
);



