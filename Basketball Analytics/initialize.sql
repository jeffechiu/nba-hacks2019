DROP DATABASE IF EXISTS Basketball;
CREATE DATABASE Basketball;

\c basketball;

\i create.sql

\copy event_codes from 'Event_Codes.csv' csv header

\copy game_lineup from 'Game_Lineup.csv' csv header

\copy play_by_play from 'Play_by_Play.csv' csv header

\copy (SELECT * FROM Play_by_Play WHERE game_id='006728e4c10e957011e1f24878e6054a') to 'game_1_quarter_1.csv' with csv header

#\copy (SELECT DISTINCT team_id FROM Play_by_Play ORDER BY team_id) to 'teams.csv' with csv header

#\copy (SELECT DISTINCT person1 FROM Play_by_Play ORDER BY person1) to 'players.csv' with csv header