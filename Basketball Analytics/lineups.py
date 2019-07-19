import csv

#reads a CSV file in DictRead format
def openCSV(file):
	game = []
	with open(file, newline='') as csvfile:
		rows = csv.DictReader(csvfile)
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in rows:
			game += [row]
	return game

#gets IDS of team
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

#gets ID of team actions in player columns
def getTeamPlayerIDS(game, t1, t2):
	tp1=""
	tp2=""
	for row in game:
		if row['event_msg_type'] == '9' and (row['action_type'] == '1' or row['action_type'] == '2') and row['team_id'] == t1:
			tp1 = row['person1']
		if row['event_msg_type'] == '9' and (row['action_type'] == '1' or row['action_type'] == '2') and row['team_id'] == t2:
			tp2 = row['person1']
	return (tp1, tp2)

#sorts event numbers
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

#recursive function that modifies game so that all necessary substitutions come after free throws
#STILL NEED TO ADD INFO ABOUT TECHNICALS
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

#get all possessions in format in array of tuples from start of possession eventnum to end of possession eventnum
def getPossessions(eventNums, game, t1, t2):
	team_poss = ""
	possessions = []
	poss = []
	for x in range(len(eventNums)):
		for row in game:
			if row['period'] == '2':
				if row['event_num'] == str(eventNums[x]):
					if team_poss == "":
						if (row['team_id'] == t1 or row['team_id'] == t2):
							poss += [row['event_num']]
							team_poss = row['team_id']
							break
						else:
							break
					elif row['event_msg_type'] == '12' and row['period'] != '1':
						poss += [row['event_num']]
						team_poss = row['team_id']
						break
					elif row['event_msg_type'] == '13':
						poss += [row['event_num']]
						possessions += [poss]
						poss = []
						break
					elif row['team_id'] != team_poss:
						team_poss = row['team_id']
						for row1 in game:
							if row1['event_num'] == str(eventNums[x-1]):
								poss += [row1['event_num']]
						possessions += [poss]
						poss = []
						poss += [row['event_num']]
						break
	return possessions

#gets lineups of game
def getLineups(eventNums, game, t1, t2, tp1, default, starters):
	lineup = []
	currLineup = ["null", "null", "null", "null", "null", "null", "null", "null", "null", t1, "null", "null"]
	for x in range(len(eventNums)):
		for row in game:
			if row['event_num'] == str(eventNums[x]):

				if row['event_msg_type'] == '8':
					if (row['person1'] == currLineup[4] or row['person1'] == currLineup[5] or row['person1'] == currLineup[6] or row['person1'] == currLineup[7] or row['person1'] == currLineup[8]):
						person = row['person1']
						currLineup[1] = row['pc_time']
						currLineup[3] = row['event_num']
						newLineup = ["null", "null", "null", "null", "null", "null", "null", "null", "null", t1, "null", "null"]
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
						currLineup[10] = row['game_id']
						currLineup[11] = row['period']
						lineup += [currLineup]
						currLineup = newLineup

				#start period
				elif row['event_msg_type'] == '12':
					currLineup[0] = row['pc_time']
					currLineup[2] = row['event_num']
					index = 4
					for start in starters:
						if start['ï»¿Game_id'] == row['game_id'] and start['Period'] == row['period'] and start['Team_id'] == t1:
							currLineup[index] = start['Person_id']
							index += 1
							if index == 9:
								break

				#end period without possession
				elif row['event_msg_type'] == '13':
					currLineup[1] = row['pc_time']
					currLineup[3] = row['event_num']
					currLineup[10] = row['game_id']
					currLineup[11] = row['period']
					lineup += [currLineup]	
					newLineup = ["null", "null", "null", "null", "null", "null", "null", "null", "null", t1, "null", "null"]
					currLineup = newLineup			
	counter = []
	for i in range(len(lineup)):
		if lineup[i][0] == lineup[i][1]:
			counter += [lineup[i]]
	for x in counter:
		lineup.remove(x)

	return lineup

#calculate score between 2 eventNums for a team
def calculateScore(t1, eventNum1, eventNum2):
	return

#get the number of possessions in range between 2 event numbers
def getNumPossessions(eventNum1, eventNum2):
	return

#create table of team_id, player_id, off_total, def_total, possessions_played
def createRatingsChart():
	return


def main():
	default = '1473d70e5646a26de3c52aa1abd85b1f'
	default1 = '0370a0d090da0d0edc6319f120187e0e'
	game = openCSV('game_1_quarter_1.csv')
	starters = openCSV('Game_Lineup.csv')
	eventNums = sortEventNums(game)
	game = modifyGame(eventNums, game)
	teamIDS = getTeamIDs(game, default)
	teamPlayerIDS = getTeamPlayerIDS(game, teamIDS[0], teamIDS[1])
	t1 = teamIDS[0]
	t2 = teamIDS[1]
	tp1 = teamPlayerIDS[0]
	tp2 = teamPlayerIDS[1]
	possessions = getPossessions(eventNums, game, t1, t2)
	print(possessions)
	print(len(possessions))
	#events = getAllEventsUsed(game)
	lineupT1 = getLineups(eventNums, game, t2, t1, tp2, default1, starters)
	lineupT2 = getLineups(eventNums, game, t1, t2, tp1, default1, starters)
	lineup = []
	lineup += [['time_s', 'time_e', 'event_s', 'event_e', 'player_1', 'player_2', 'player_3', 'player_4', 'player_5', 'team_id', 'game_id', 'period']]
	for line in lineupT1:
		lineup += [line]
	for line in lineupT2:
		lineup += [line]

	with open('lineups.csv', 'w', newline='') as csvFile:
	    writer = csv.writer(csvFile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    writer.writerows(lineup)
	    print("Successfully exported into lineups.csv")

if __name__ == "__main__":
	main()
