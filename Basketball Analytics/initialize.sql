DROP DATABASE IF EXISTS Basketball;
CREATE DATABASE Basketball;

\c basketball;

\i create.sql

\copy event_codes from 'Event_Codes.csv' csv

\copy game_lineup from 'Game_Lineup.csv' csv

\copy play_by_play from 'Play_by_Play.csv' csv