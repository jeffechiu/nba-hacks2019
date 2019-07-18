import csv

def openCSV(file):
	game = []
	with open(file, newline='') as csvfile:
		rows = csv.DictReader(csvfile)
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in rows:
			game += [row]
	return game
#game = list(csv.reader(open('game_1_quarter_1.csv')))

def getTeamIDs(game, default):
	t1 = ""
	t2 = ""
	for row in game:
		#initialize team variables
		if t1 == "" and row['team_id'] != default:
			t1 = row['team_id']
		if t1 != row['team_id'] and t2 == "" and row['team_id'] != default:
			t2 = row['team_id']
	return (t1, t2)

def getTeamPlayerIDS(game, t1, t2):
	tp1=""
	tp2=""
	for row in game:
		if row['event_msg_type'] == '9' and (row['action_type'] == '1' or row['action_type'] == '2') and row['team_id'] == t1:
			tp1 = row['person1']
		if row['event_msg_type'] == '9' and (row['action_type'] == '1' or row['action_type'] == '2') and row['team_id'] == t2:
			tp2 = row['person1']
	return (tp1, tp2)

def sortEventNums(game):
	eventNums = []
	for row in game:
		eventNums += [int(row['event_num'])]
	eventNums = sorted(eventNums)
	return eventNums

def getAllEventsUsed(game):
	events = []
	for row in game:
		if int(row['event_msg_type']) not in events:
			events += [int(row['event_msg_type'])]
	events = sorted(events)
	return events

def getNumPossessions(eventNums, game):
	possessions = 0
	team_poss = ""
	for x in range(len(eventNums)):
		for row in game:
			if row['event_num'] == str(eventNums[x]):
				if x == 0:
					team_poss = row['team_id']
				elif row['team_id'] != team_poss:
					team_poss = row['team_id']
					possessions += 1
				break
	return possessions

def modifyGame(eventNums, game):
	changes = 0
	nums = []
	for x in range(len(eventNums)):
		for row in game:
			if row['event_num'] == str(eventNums[x]):
				if row['event_msg_type'] == '8':
					for row1 in game:
						if row1['event_num'] == str(eventNums[x+1]):
							if row1['event_msg_type'] == '3':
								changes += 1
								nums += [(eventNums[x], eventNums[x+1])]
	if changes == 0:
		return game
	else:
		for num in range(len(nums)):
			for row2 in game:
				if row2['event_num'] == str(nums[num][0]) and row2['event_msg_type'] == '8':
					row2['event_num'] = str(nums[num][1])
				if row2['event_num'] == str(nums[num][1]) and row2['event_msg_type'] == '3':
					row2['event_num'] = str(nums[num][0])
		return modifyGame(eventNums, game)

def getLineups(eventNums, game, t1, t2, tp1, default):
	lineup = []
	currLineup = ["null", "null", "null", "null", "null", "null", "null", "null", "null", t1]
	lineup += [['time_s', 'time_e', 'event_s', 'event_e', 'player_1', 'player_2', 'player_3', 'player_4', 'player_5']]
	for x in range(len(eventNums)):
		for row in game:
			if row['event_num'] == str(eventNums[x]):

				#currently own possession
				if row['team_id'] == t1:

					#made a bucket, assisted
					if row['event_msg_type'] == '1':
						if currLineup[4] == "null":
							currLineup[4] = row['person1']
						elif currLineup[5] == "null" and currLineup[4] != row['person1']:
							currLineup[5] = row['person1']
						elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
							currLineup[6] = row['person1']
						elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
							currLineup[7] = row['person1']
						elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
							currLineup[8] = row['person1']
						if row['person2'] != default:
							if currLineup[4] == "null":
								currLineup[4] = row['person2']
							elif currLineup[5] == "null" and currLineup[4] != row['person2']:
								currLineup[5] = row['person2']
							elif currLineup[6] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2']:
								currLineup[6] = row['person2']
							elif currLineup[7] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2']:
								currLineup[7] = row['person2']
							elif currLineup[8] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2'] and currLineup[7] != row['person2']:
								currLineup[8] = row['person2']

					#missed a bucket and free throw
					elif row['event_msg_type'] == '2' or row['event_msg_type'] == '3':
						if currLineup[4] == "null":
							currLineup[4] = row['person1']
						elif currLineup[5] == "null" and currLineup[4] != row['person1']:
							currLineup[5] = row['person1']
						elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
							currLineup[6] = row['person1']
						elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
							currLineup[7] = row['person1']
						elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
							currLineup[8] = row['person1']

					#offensive rebound
					elif row['event_msg_type'] == '4' and row['person1'] != tp1:
						for row1 in game:
							if row1['event_num'] == str(eventNums[x+1]):
								if row1['team_id'] == t1:
									if currLineup[4] == "null":
										currLineup[4] = row['person1']
									elif currLineup[5] == "null" and currLineup[4] != row['person1']:
										currLineup[5] = row['person1']
									elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
										currLineup[6] = row['person1']
									elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
										currLineup[7] = row['person1']
									elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
										currLineup[8] = row['person1']

					#turnover
					elif row['event_msg_type'] == '5' and row['person1'] != tp1:
						if currLineup[4] == "null":
							currLineup[4] = row['person1']
						elif currLineup[5] == "null" and currLineup[4] != row['person1']:
							currLineup[5] = row['person1']
						elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
							currLineup[6] = row['person1']
						elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
							currLineup[7] = row['person1']
						elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
							currLineup[8] = row['person1']

					#offensive foul and opposing defensive foul
					elif row['event_msg_type'] == '6' and row['person1'] != tp1:
						for row1 in game:
							if row1['event_num'] == str(eventNums[x+1]):
								if row1['team_id'] == t2:
									if currLineup[4] == "null":
										currLineup[4] = row['person1']
									elif currLineup[5] == "null" and currLineup[4] != row['person1']:
										currLineup[5] = row['person1']
									elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
										currLineup[6] = row['person1']
									elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
										currLineup[7] = row['person1']
									elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
										currLineup[8] = row['person1']
								elif row1['team_id'] == t1:
									if currLineup[4] == "null":
										currLineup[4] = row['person2']
									elif currLineup[5] == "null" and currLineup[4] != row['person2']:
										currLineup[5] = row['person2']
									elif currLineup[6] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2']:
										currLineup[6] = row['person2']
									elif currLineup[7] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2']:
										currLineup[7] = row['person2']
									elif currLineup[8] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2'] and currLineup[7] != row['person2']:
										currLineup[8] = row['person2']

					#substitution, reset lineups
					elif row['event_msg_type'] == '8':
						if (row['person1'] == currLineup[4] or row['person1'] == currLineup[5] or row['person1'] == currLineup[6] or row['person1'] == currLineup[7] or row['person1'] == currLineup[8]):
							person = row['person1']
							currLineup[1] = row['pc_time']
							currLineup[3] = row['event_num']
							newLineup = ["null", "null", "null", "null", "null", "null", "null", "null", "null", t1]
							newLineup[0] = row['pc_time']
							newLineup[2] = row['event_num']
							if person == currLineup[4]:
								newLineup[4] = row['person2']
							else:
								newLineup[4] = currLineup[4]

							if person == currLineup[5]:
								newLineup[5] = row['person2']
							else:
								newLineup[5] = currLineup[5]
							
							if person == currLineup[6]:
								newLineup[6] = row['person2']
							else:
								newLineup[6] = currLineup[6]
							
							if person == currLineup[7]:
								newLineup[7] = row['person2']
							else:
								newLineup[7] = currLineup[7]

							if person == currLineup[8]:
								newLineup[8] = row['person2']
							else:
								newLineup[8] = currLineup[8]
							lineup += [currLineup]
							currLineup = newLineup

					#jump ball, win jump and gain possession
					elif row['event_msg_type'] == '10':
						if currLineup[4] == "null":
							currLineup[4] = row['person1']
						elif currLineup[5] == "null" and currLineup[4] != row['person1']:
							currLineup[5] = row['person1']
						elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
							currLineup[6] = row['person1']
						elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
							currLineup[7] = row['person1']
						elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
							currLineup[8] = row['person1']

						if currLineup[5] == "null" and currLineup[4] != row['person3']:
							currLineup[5] = row['person3']
						elif currLineup[6] == "null" and currLineup[4] != row['person3'] and currLineup[5] != row['person3']:
							currLineup[6] = row['person3']
						elif currLineup[7] == "null" and currLineup[4] != row['person3'] and currLineup[5] != row['person3'] and currLineup[6] != row['person3']:
							currLineup[7] = row['person3']
						elif currLineup[8] == "null" and currLineup[4] != row['person3'] and currLineup[5] != row['person3'] and currLineup[6] != row['person3'] and currLineup[7] != row['person3']:
							currLineup[8] = row['person3']

					#end period
					elif row['event_msg_type'] == '13':
						currLineup[1] = row['pc_time']
						currLineup[3] = row['event_num']
						lineup += [currLineup]

				else:

					#blocked shot
					if row['event_msg_type'] == '2' and row['person3'] != default:
						if currLineup[4] == "null":
							currLineup[4] = row['person3']
						elif currLineup[5] == "null" and currLineup[4] != row['person3']:
							currLineup[5] = row['person3']
						elif currLineup[6] == "null" and currLineup[4] != row['person3'] and currLineup[5] != row['person3']:
							currLineup[6] = row['person3']
						elif currLineup[7] == "null" and currLineup[4] != row['person3'] and currLineup[5] != row['person3'] and currLineup[6] != row['person3']:
							currLineup[7] = row['person3']
						elif currLineup[8] == "null" and currLineup[4] != row['person3'] and currLineup[5] != row['person3'] and currLineup[6] != row['person3'] and currLineup[7] != row['person3']:
							currLineup[8] = row['person3']

					#defensive rebound
					elif row['event_msg_type'] == '4' and row['person1'] != tp1:
						for row1 in game:
							if row1['event_num'] == str(eventNums[x+1]):
								if row1['team_id'] == t1:
									if currLineup[4] == "null":
										currLineup[4] = row['person1']
									elif currLineup[5] == "null" and currLineup[4] != row['person1']:
										currLineup[5] = row['person1']
									elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
										currLineup[6] = row['person1']
									elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
										currLineup[7] = row['person1']
									elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
										currLineup[8] = row['person1']

					#steal
					elif row['event_msg_type'] == '5' and row['person2'] != default and row['person2'] != tp1:
						if currLineup[4] == "null":
							currLineup[4] = row['person2']
						elif currLineup[5] == "null" and currLineup[4] != row['person2']:
							currLineup[5] = row['person2']
						elif currLineup[6] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2']:
							currLineup[6] = row['person2']
						elif currLineup[7] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2']:
							currLineup[7] = row['person2']
						elif currLineup[8] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2'] and currLineup[7] != row['person2']:
							currLineup[8] = row['person2']

					#defensive foul and opposing offensive foul
					elif row['event_msg_type'] == '6' and row['person1'] != tp1:
						for row1 in game:
							if row1['event_num'] == str(eventNums[x+1]):
								if row1['team_id'] == t2:
									if currLineup[4] == "null":
										currLineup[4] = row['person1']
									elif currLineup[5] == "null" and currLineup[4] != row['person1']:
										currLineup[5] = row['person1']
									elif currLineup[6] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1']:
										currLineup[6] = row['person1']
									elif currLineup[7] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1']:
										currLineup[7] = row['person1']
									elif currLineup[8] == "null" and currLineup[4] != row['person1'] and currLineup[5] != row['person1'] and currLineup[6] != row['person1'] and currLineup[7] != row['person1']:
										currLineup[8] = row['person1']
								elif row1['team_id'] == t1:
									if currLineup[4] == "null":
										currLineup[4] = row['person2']
									elif currLineup[5] == "null" and currLineup[4] != row['person2']:
										currLineup[5] = row['person2']
									elif currLineup[6] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2']:
										currLineup[6] = row['person2']
									elif currLineup[7] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2']:
										currLineup[7] = row['person2']
									elif currLineup[8] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2'] and currLineup[7] != row['person2']:
										currLineup[8] = row['person2']

					#substitution, reset
					elif row['event_msg_type'] == '8':
						if (row['person1'] == currLineup[4] or row['person1'] == currLineup[5] or row['person1'] == currLineup[6] or row['person1'] == currLineup[7] or row['person1'] == currLineup[8]):
							person = row['person1']
							currLineup[1] = row['pc_time']
							currLineup[3] = row['event_num']
							newLineup = ["null", "null", "null", "null", "null", "null", "null", "null", "null", t1]
							newLineup[0] = row['pc_time']
							newLineup[2] = row['event_num']
							if person == currLineup[4]:
								newLineup[4] = row['person2']
							else:
								newLineup[4] = currLineup[4]

							if person == currLineup[5]:
								newLineup[5] = row['person2']
							else:
								newLineup[5] = currLineup[5]
							
							if person == currLineup[6]:
								newLineup[6] = row['person2']
							else:
								newLineup[6] = currLineup[6]
							
							if person == currLineup[7]:
								newLineup[7] = row['person2']
							else:
								newLineup[7] = currLineup[7]

							if person == currLineup[8]:
								newLineup[8] = row['person2']
							else:
								newLineup[8] = currLineup[8]
							lineup += [currLineup]
							currLineup = newLineup

					#jump ball, lost jump
					elif row['event_msg_type'] == '10':
						if currLineup[4] == "null":
							currLineup[4] = row['person2']
						elif currLineup[5] == "null" and currLineup[4] != row['person2']:
							currLineup[5] = row['person2']
						elif currLineup[6] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2']:
							currLineup[6] = row['person2']
						elif currLineup[7] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2']:
							currLineup[7] = row['person2']
						elif currLineup[8] == "null" and currLineup[4] != row['person2'] and currLineup[5] != row['person2'] and currLineup[6] != row['person2'] and currLineup[7] != row['person2']:
							currLineup[8] = row['person2']

					#start period
					elif row['event_msg_type'] == '12':
						currLineup[0] = row['pc_time']
						currLineup[2] = row['event_num']

					#end period without possession
					elif row['event_msg_type'] == '13':
						currLineup[1] = row['pc_time']
						currLineup[3] = row['event_num']
						lineup += [currLineup]				
	counter = []
	for i in range(len(lineup)):
		if lineup[i][0] == lineup[i][1]:
			counter += [lineup[i]]
	for x in counter:
		lineup.remove(x)

	return lineup



def main():
	default = '1473d70e5646a26de3c52aa1abd85b1f'
	default1 = '0370a0d090da0d0edc6319f120187e0e'
	game = openCSV('game_1_quarter_1.csv')
	eventNums = sortEventNums(game)
	possessions = getNumPossessions(eventNums, game)
	#print(possessions, "possessions")
	game = modifyGame(eventNums, game)
	teamIDS = getTeamIDs(game, default)
	teamPlayerIDS = getTeamPlayerIDS(game, teamIDS[0], teamIDS[1])
	t1 = teamIDS[0]
	print(t1)
	t2 = teamIDS[1]
	tp1 = teamPlayerIDS[0]
	tp2 = teamPlayerIDS[1]
	#print(teamIDS)
	#print(teamPlayerIDS)
	#lineup = getLineupsT1(eventNums, game, t1, tp1)
	events = getAllEventsUsed(game)
	lineupT1 = getLineups(eventNums, game, t2, t1, tp2, default1)
	lineupT2 = getLineups(eventNums, game, t1, t2, tp1, default1)
	for row in lineupT1:
		print(row)
	for row in lineupT2:
		print(row)

if __name__ == "__main__":
	main()
