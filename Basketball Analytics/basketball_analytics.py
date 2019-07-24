import csv
import sys
from data import *
from game import *

def run_pbp(pbp, ev_codes, game_lineups, games_obj):
  for game_id in pbp:
    game = pbp[game_id]
    game_data = games_obj[game_id]
    for quarter in game:
      for play in game[quarter]:
        if play["event_type"] == "6":
          print_play(play, quarter, game_id, ev_codes)
        run_play(play, game_data, quarter, game_lineups)

def run_play(play, game, period, lineups):
  event_type = play["event_type"]
  action_type = play["action_type"]
  op1 = play["option1"]
  team = play["team_id"]
  p1 = play["person1"]
  p2 = play["person2"]

  if event_type == "12": #start of period
    game.update_lineup(lineups[game.id][period])

  elif event_type == "8": #substitutions
    if game.delay_subs:
      game.queued_subs.add((p1, p2))
    else:
      game.substitute(p1, p2)

  # elif event_type == "6": #fouls
  #   if op1 != "0":
  #     game.delay_subs = True

  elif event_type == "5": #turnovers
    game.update(team)

  elif event_type == "4": #rebounds
    game.update(team)

  elif event_type == "3": #free throws
    ends = ["10","12","15","16","17","19","20","22","26","29"] # the "x of x" free throws
    if action_type in ends:
      game.delay_subs = False
      game.do_queued_subs()
    game.update(team, op1)

  elif event_type == "1": #made shots
    game.update(team, op1)

def write_output(output, games_obj):
  final = [["Game_ID", "Player_ID", "OffRtg", "DefRtg"]]

  for game in games_obj:
    for player in games_obj[game].players_appeared:
      player_obj = games_obj[game].players_appeared[player]
      final += [[player_obj.game_id, player_obj.id, str(player_obj.off_rtg()),
                  str(player_obj.def_rtg())]]

  with open(output, "w", newline = "") as fp:
    a = csv.writer(fp, delimiter = ',')
    a.writerows(final)

#for debugging purposes
def print_play(play, period, game, ev_codes=None):
  event_type, action_type = play["event_type"], play["action_type"]
  pc_time = play["pc_time"]
  team_id, p1 = play["team_id"], play["person1"]
  try:
    play_type = ev_codes[(event_type, action_type)]
  except:
    play_type = event_type + ", " + action_type
  minutes = str(int((int(pc_time)/10)//60))
  seconds = str((int(pc_time)/10)%60)
  if seconds.index(".") == 1: seconds = "0" + seconds
  if seconds[-1] == "0": seconds = seconds[:-2]
  print("Game: " + game + " Period", period, ":", minutes + ":" + seconds, team_id + " --", p1, play_type)

def main():
  ev_codes = make_ev_dict(sys.argv[1])
  game_lineups = get_lineups(sys.argv[2])
  games_obj = games_init(game_lineups)
  play_by_play = convert_pbp(sys.argv[3])
  run_pbp(play_by_play, ev_codes, game_lineups, games_obj)
  write_output(sys.argv[4], games_obj)

#run this:
#python basketball_analytics.py Event_Codes.csv Game_Lineup.csv Play_by_Play.csv Your_Team_Name_Q1_BBALL.csv
if __name__ == "__main__":
  main()