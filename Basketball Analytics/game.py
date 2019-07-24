class Game(object):
  def __init__(self, game_id, team1="", team2=""):
    self.id = game_id
    self.team1 = team1
    self.team2 = team2
    self.delay_subs = False
    self.queued_subs = set()
    self.players_appeared = dict()
    self.team1_poss = True #to keep track of possession
    self.first_jump = False
    self.tip_winner = False #whether the initial winner of the jump ball is team1
    self.reset_personals()

  #for debugging purposes
  def __repr__(self):
    return self.id

  def __hash__(self):
    return hash(self.id)

  def __eq__(self, other):
    return (isinstance(other, Game) and (self.id == other.id))

  #creates a player and adds him to self.players_appeared
  def create_player(self, pid, team):
    if pid in self.players_appeared:
      return
    self.players_appeared[pid] = Player(pid, self.id, team)

  #updates lineups at the start of periods
  def update_lineup(self, lineups):
    t1_lineup = set(lineups[self.team1])
    t2_lineup = set(lineups[self.team2])

    #starts by resetting all current players to not be on the court
    for player in self.players_appeared:
      self.players_appeared[player].in_game = False

    #next two loops used to create players that haven't appeared in the game yet
    for player in t1_lineup:
      self.create_player(player, self.team1)
    for player in t2_lineup:
      self.create_player(player, self.team2)

    #marks everyone subbed in at the beginning of the period as on the court
    for person in t1_lineup.union(t2_lineup):
      self.players_appeared[person].in_game = True

  #handles substitutions
  def substitute(self, player_out, player_in):
    team = self.players_appeared[player_out].team #makes sure the two players are on the same team
    self.create_player(player_in, team) #player objects are created for players that haven't appeared yet
    self.players_appeared[player_out].in_game = False
    self.players_appeared[player_in].in_game = True

  #handles queued substitutions after free throws
  def do_queued_subs(self):
    for sub in self.queued_subs: #sub: (player_out, player_in)
      self.substitute(sub[0], sub[1])
    self.queued_subs = set()

  #handles updating players' data when points are scored
  def update(self, team, points=0):
    for pid in self.players_appeared:
      player = self.players_appeared[pid]
      if player.team == team:
        player.off_poss()
        player.off_score(points)
      else:
        player.def_poss()
        player.def_score(points)
    self.flip_possession()

  #changes possession
  def flip_possession(self):
    self.team1_poss = not self.team1_poss

  #resets team personal foul counts at beginning of periods
  def reset_personals(self):
    self.personal_fouls = {self.team1: 0, self.team2: 0}

  #for debugging, counts number of player with in_game == True (total, team1, team2)
  def count_on_court(self):
    count = 0
    t1_count = 0
    t2_count = 0
    for player in self.players_appeared:
      if self.players_appeared[player].in_game:
        count += 1
        if self.players_appeared[player].team == self.team1:
          t1_count += 1
        if self.players_appeared[player].team == self.team2:
          t2_count += 1
    return count, t1_count, t2_count

###############################################################################

class Player(object):
  def __init__(self, person_id, game_id, team):
    self.id = person_id
    self.game_id = game_id
    self.team = team
    self.off_possessions = 0
    self.def_possessions = 0
    self.off_points = 0
    self.def_points = 0
    self.in_game = False

  #for debugging purposes
  def __repr__(self):
    return self.id

  def __hash__(self):
    return hash((self.id, self.game_id))

  def __eq__(self, other):
    return (isinstance(other, Player) and (self.id == other.id) 
      and (self.game_id == other.game_id))

  def off_poss(self):
    if self.in_game:
      self.off_possessions += 1

  def def_poss(self):
    if self.in_game:
      self.def_possessions += 1

  def off_score(self, points=0):
    if self.in_game:
      self.off_points += points

  def def_score(self, points=0):
    if self.in_game:
      self.def_points += points

  def off_rtg(self):
    if self.off_possessions == 0:
      return 0
    else:
      return self.off_points * (100/self.off_possessions)

  def def_rtg(self):
    if self.def_possessions == 0:
      return 0
    else:
      return self.def_points * (100/self.def_possessions)