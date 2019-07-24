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
        print_play(play, quarter, game_id, ev_codes)
        run_play(play, game_data, quarter, game_lineups) 

def run_play(play, game, period, lineups):
  event_type = play["event_type"]
  action_type = play["action_type"]
  op1 = play["option1"]
  team = play["team_id"]
  p1 = play["person1"]
  p2 = play["person2"]

  if event_type == "13": #end of period
    game.update(team)

  elif event_type == "12": #start of period
    game.update_lineup(lineups[game.id][period])
    if period == 2 or period == 3:
      game.team1_poss = not game.tip_winner
    elif period == 4:
      game.team1_poss = game.tip_winner
    game.reset_personals()

  elif event_type == "10": #jump balls
    is_team1 = team == game.team1
    game.team1_poss = (is_team1)
    if not game.first_jump:
      game.first_jump = True
      game.tip_winner = is_team1

  elif event_type == "8": #substitutions
    if game.delay_subs:
      game.queued_subs.add((p1, p2))
    else:
      game.substitute(p1, p2)

  elif event_type == "6": #fouls
    if action_type == "2" or action_type == "29":
      game.delay_subs = True
    #personal or technical fouls
    elif int(action_type) == 1 or (10 <= int(action_type) and int(action_type) <= 28):
      game.personal_fouls[team] += 1
      if game.personal_fouls[team] > 5:
        game.delay_subs = True

  elif event_type == "5": #turnovers
    game.update(team)

  elif event_type == "4": #rebounds
    if (team == game.team1 and not game.team1_poss):
      game.update(team)
    elif (team == game.team2 and game.team1_poss):
      game.update(team)

  elif event_type == "3": #free throws
    ends = ["10","12","15","16","17","19","20","22","26","29"] # the "x of x" free throws
    game.update(team, op1)
    if action_type in ends:
      game.delay_subs = False
      game.do_queued_subs()

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
  play_type = ev_codes[(event_type, action_type)]
  minutes = str(int((int(pc_time)/10)//60))
  seconds = str((int(pc_time)/10)%60)
  if seconds.index(".") == 1: seconds = "0" + seconds
  if seconds[-1] == "0": seconds = seconds[:-2]
  print("Game: " + game + " Period", period, ":", minutes + ":" + seconds, team_id + " --", p1, play_type)

#to visualize the event codes
def print_ev_codes(ev_codes):
  for code in ev_codes:
    print(code, ev_codes[code])

def main():
  ev_codes = make_ev_dict(sys.argv[1])
  game_lineups = get_lineups(sys.argv[2])
  games_obj = games_init(game_lineups)
  play_by_play = convert_pbp(sys.argv[3])
  run_pbp(play_by_play, ev_codes, game_lineups, games_obj)
  write_output(sys.argv[4], games_obj)

  # print_ev_codes(ev_codes)

#run this:
#python basketball_analytics.py Event_Codes.csv Game_Lineup.csv Play_by_Play.csv Your_Team_Name_Q1_BBALL.csv
if __name__ == "__main__":
  main()