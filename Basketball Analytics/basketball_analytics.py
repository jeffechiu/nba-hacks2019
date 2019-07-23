import csv
import sys
from data import *
from game import *

#for debugging purposes
def print_event(play, period, game, ev_codes):
  event_type, action_type = play["event_type"], play["action_type"]
  pc_time = play["pc_time"]
  team_id, p1 = play["team_id"], play["person1"]
  play_type = ev_codes[(event_type, action_type)]
  minutes = str(int((int(pc_time)/10)//60))
  seconds = str((int(pc_time)/10)%60)
  if seconds.index(".") == 1: seconds = "0" + seconds
  if seconds[-1] == "0": seconds = seconds[:-2]
  print("Game: " + game + " Period", period, ":", minutes + ":" + seconds, team_id + " --", p1, play_type)

def main():
  ev_codes = make_ev_dict(sys.argv[1])
  game_lineups = get_lineups(sys.argv[2])
  play_by_play = convert_pbp(sys.argv[3])

  for game in play_by_play:
    for period in play_by_play[game]:
      for play in play_by_play[game][period]:
        print_event(play, period, game, ev_codes)

    break

  output = sys.argv[4]

if __name__ == "__main__":
  main()