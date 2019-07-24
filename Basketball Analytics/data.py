import csv
from game import *

#code to turn the event codes csv file into a more usable dictionary format
#ev_dict[(msg_type, action_type)] = msg_desc: action_desc
def make_ev_dict(ev_raw):
  ev_dict = dict()
  with open(ev_raw, newline='') as f:
    ev_codes = csv.reader(f)

    for row in ev_codes:
      msg_type = row[0]
      if len(msg_type) > 4:
        continue
      action_type = row[1]
      msg_desc = row[2].strip()
      action_desc = row[3].strip()

      key = (msg_type, action_type)
      val = msg_desc + ": " + action_desc
      ev_dict[key] = val

  return ev_dict

#function that turns the game lineups csv file into a more usable dictionary format
#lineups_dict[game_id][period][team_id] = [list of person_id's]
def get_lineups(lineups_raw):
  lineups_dict = dict()
  with open(lineups_raw, newline='') as f:
    game_lineups = csv.reader(f)

    for row in game_lineups:
      game_id = row[0]
      try:
        period = int(row[1])
      except:
        continue
      person_id = row[2]
      team_id = row[3]
      status = row[4]

      if game_id not in lineups_dict:
        lineups_dict[game_id] = dict()
      game_dict = lineups_dict[game_id]
      if period not in game_dict:
        game_dict[period] = dict()
      period_dict = game_dict[period]
      if team_id not in period_dict:
        period_dict[team_id] = []
      team_list = period_dict[team_id]
      if status != "I":
        team_list.append(person_id)

  return lineups_dict

#initializes game objects
def games_init(lineups):
  games_dict = dict()
  for game_id in lineups:
    teams = list(lineups[game_id][0].keys())
    games_dict[game_id] = Game(game_id, teams[0], teams[1])
  return games_dict

#function to do insertion sort 
def pbp_sort(pbp_quarter): 
  for i in range(1, len(pbp_quarter)): 
    play = pbp_quarter[i]
    j = i-1
    while (j>=0) and (play["pc_time"] > pbp_quarter[j]["pc_time"]): 
      pbp_quarter[j+1] = pbp_quarter[j] 
      j -= 1
    pbp_quarter[j+1] = play

#creates play-by-play dictionaries, broken up by game and then period
def convert_pbp(pbp_raw):
  games_pbp = dict()
  with open(pbp_raw, newline='') as f:
    pbp = csv.reader(f)

    for row in pbp:
      game_id = row[0]
      event_num = row[1]
      event_msg_type = row[2]
      try:
        period = int(row[3])
      except:
        continue

      if game_id not in games_pbp:
        games_pbp[game_id] = dict()
      game = games_pbp[game_id]
      if period not in game:
        game[period] = []
      play = {"event_num": event_num,
              "event_type": event_msg_type,
              "period": period,
              "wc_time": int(row[4]),
              "pc_time": int(row[5]),
              "action_type": row[6],
              "option1": int(row[7]),
              "team_id": row[10],
              "person1": row[11],
              "person2": row[12]}
      game[period].append(play)

  for game in games_pbp:
    for per in games_pbp[game]:
      pbp_sort(games_pbp[game][per])

  return games_pbp