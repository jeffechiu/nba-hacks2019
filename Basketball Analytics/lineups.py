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

#takes array of all pbp, returns list of games(82)
def getGames(gameList):
	return


def parseGames(game):
	return

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
			break
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

#def getAllEventsUsed(game):
#	events = []
#	for row in game:
#		if int(row['event_msg_type']) not in events:
#			events += [int(row['event_msg_type'])]
#	events = sorted(events)
#	return events

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
			if row['event_num'] == str(eventNums[x]):
				if team_poss == "":
					if (row['team_id'] == t1 or row['team_id'] == t2):
						poss += [int(row['event_num'])]
						team_poss = row['team_id']
						break
					else:
						break
				elif row['event_msg_type'] == '12' and int(row['period']) > 1 and int(row['period']) < 5:
					poss += [int(row['event_num'])]
					team_poss = row['team_id']
					break
				elif row['event_msg_type'] == '13':
					poss += [int(row['event_num'])]
					poss += [team_poss]
					possessions += [poss]
					poss = []
					break
				elif row['team_id'] != team_poss:
					for row1 in game:
						if row1['event_num'] == str(eventNums[x-1]):
							poss += [int(row1['event_num'])]
					poss += [team_poss]
					possessions += [poss]
					poss = []
					poss += [int(row['event_num'])]
					team_poss = row['team_id']
					break
	return possessions

def getOffPoss(possessions, t1):
	final = []
	for poss in possessions:
		if poss[2] == t1:
			final += [poss]
	return final

def getDefPoss(possessions, t1):
	final = []
	for poss in possessions:
		if poss[2] != t1:
			final += [poss]
	return final

#get the number of possessions in range between 2 event numbers
def getNumPossessions(eventNum1, eventNum2, possessions):
	en1 = int(eventNum1)
	en2 = int(eventNum2)
	p = 0
	for poss in possessions:
		if poss[0] <= en1 and poss[1] >= en1:
			p = 1
		elif p == 0:
			continue
		elif poss[0] > en2:
			return p
		elif poss[0] < en2:
			p += 1
	return p

def getOffPossessions(eventNum1, eventNum2, possessions, t1):
	en1 = int(eventNum1)
	en2 = int(eventNum2)
	p = 0
	active = "false"
	for poss in possessions:
		if poss[2] == t1:
			if poss[0] <= en1 and poss[1] >= en1:
				p = 1
				active = "true"
			elif poss[0] > en2 and active == "true":
				return p
			elif poss[0] < en2 and active == "true":
				p += 1
		else:
			if poss[0] <= en1 and poss[1] >= en1:
				active = "true"
	return p

def getDefPossessions(eventNum1, eventNum2, possessions, t1):
	en1 = int(eventNum1)
	en2 = int(eventNum2)
	p = 0
	active = "false"
	for poss in possessions:
		if poss[2] != t1:
			if poss[0] <= en1 and poss[1] >= en1:
				p = 1
				active = "true"
			elif poss[0] > en2 and active == "true":
				return p
			elif poss[0] < en2 and active == "true":
				p += 1
		else:
			if poss[0] <= en1 and poss[1] >= en1:
				active = "true"
	return p

def getPoints(eventNums, game):
	points = []
	basket = []
	for x in range(len(eventNums)):
		for row in game:
			if row['event_num'] == str(eventNums[x]):
				if row['event_msg_type'] == '1' or (row['event_msg_type'] == '3' and row['option1'] == '1'):
					basket += [int(row['option1'])]
					basket += [row['team_id']]
					basket += [int(row['event_num'])]
					points += [basket]
					basket = []
	return points

def getOffDef(points, eventNum1, eventNum2, t1):
	offense = 0
	defense = 0
	en1 = int(eventNum1)
	en2 = int(eventNum2)
	for point in points:
		if point[2] >= en1 and point[2] <= en2:
			if t1 == point[1]:
				offense += point[0]
			elif t1 != point[1]:
				defense += point[0]
		elif point[2] < en1:
			continue
		elif point[2] > en2:
			break
	return [offense, defense]


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
					if row['team_id'] != '1473d70e5646a26de3c52aa1abd85b1f':
						currLineup[0] = row['pc_time']
						currLineup[2] = row['event_num']
					elif row['team_id'] :
						for row1 in game:
							if row1['event_num'] == str(eventNums[x+1]):
								currLineup[0] = row1['pc_time']
								currLineup[2] = row1['event_num']
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

	for line in lineup:
		if line[0] != '7200':
			line[2] = str(int(line[2])+1)


	return lineup

def ftSubNums(game, eventNums):
	allSubs = []
	curr = []
	for x in range(len(eventNums)):
		for row in game:
			if row['event_num'] == str(eventNums[x]):
				if row['event_msg_type'] == '3':
					for row1 in game:
						if row1['event_num'] == str(eventNums[x+1]) and row1['event_msg_type'] == '8':
							curr += [row1['event_num']]
							i = 2
							num = row1['event_num']
							for row2 in game:
								if row2['event_num'] == str(eventNums[x+i]):
									if row2['event_msg_type'] != '8':
										curr += [num]
										allSubs += [curr]
										curr = []
										break
									else:
										i += 1
										num = row2['event_num']
							break

	return allSubs


#create table of team_id, player_id, game_id, period, event_num_sub, off_total, def_total, off_poss, def_poss
def createTotals(lineup, possessions, game, eventNums, points):
	ftSubs = ftSubNums(game, eventNums)
	performance = []
	row = []
	for l in range(len(lineup)):
		poss = getNumPossessions(lineup[l][2], lineup[l][3], possessions)
		offPoss = getOffPossessions(lineup[l][2], lineup[l][3], possessions, lineup[l][9])
		defPoss = getDefPossessions(lineup[l][2], lineup[l][3], possessions, lineup[l][9])
		for i in range(4, 9):
			offense = getOffDef(points, lineup[l][2], lineup[l][3], lineup[l][9])[0]
			defense = getOffDef(points, lineup[l][2], lineup[l][3], lineup[l][9])[1]
			if l != 0:
				row += [lineup[l][9], lineup[l][i], lineup[l][10], lineup[l][11], lineup[l-1][3], offense, defense, offPoss, defPoss, poss]
			else:
				row += [lineup[l][9], lineup[l][i], lineup[l][10], lineup[l][11], "null", offense, defense, offPoss, defPoss, poss]
			performance += [row]
			row = []
	for j in range(5, len(performance)):
		if performance[j][1] == performance[j-5][1] and performance[j][2] == performance[j-5][2] and performance[j][3] == performance[j-5][3]:
			offSubs = getOffPoss(possessions, performance[j][0])
			#print(offSubs)
			defSubs = getDefPoss(possessions, performance[j][0])
			#print(defSubs)
			for oSub in offSubs:
				if int(performance[j][4]) >= oSub[0] and int(performance[j][4]) <= oSub[1]:
					pns = "off"
			for dSub in defSubs:
				if int(performance[j][4]) >= dSub[0] and int(performance[j][4]) <= dSub[1]:
					pns = "def"
			for sub in ftSubs:
				if int(performance[j][4]) >= int(sub[0]) and int(performance[j][4]) <= int(sub[1]):
					 performance[j][9] += 1
					 if pns == "off":
					 	performance[j][7] += 1
					 elif pns == "def":
					 	performance[j][8] += 1
			performance[j][9] -= 1
			if pns == "off":
				performance[j][7] -= 1
			elif pns == "def":
				performance[j][8] -= 1
	return performance

#TO BE LARGELY EDITED
def removeDupes(performance):
	unique = []
	for row in performance:
		if row[1] not in unique:
			unique += [row[1]]
		else:
			i = unique.index(row[1])
			performance[i][5] += row[5]
			performance[i][6] += row[6]
			performance[i][7] += row[7]
			performance[i][8] += row[8]
			performance[i][9] += row[9]
			performance.remove(row)
			return removeDupes(performance)
	for row1 in performance:
		row1.pop(3)
		row1.pop(3)
	return performance


def accumulate():
	return

def writeCSV(file, array):
	with open(file, 'w', newline='') as csvFile:
	    writer = csv.writer(csvFile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    writer.writerows(array)
	return

def displayGame(game):
	final = []
	line = []
	final += [['event_num', 'event_msg_type', 'pc_time', 'action_type', 'person1', 'person2']]
	for row in game:
		line += [row['event_num']]
		line += [row['event_msg_type']]
		line += [row['pc_time']]
		line += [row['action_type']]
		line += [row['person1']]
		line += [row['person2']]
		final += [line]
		line = []
	return final

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
	#print(possessions)
	offSubs = getOffPoss(possessions, t1)
	#print(offSubs)
	#print(getNumPossessions('544', '584', possessions))
	points = getPoints(eventNums, game)
	#print(points)
	#print(possessions)
	#events = getAllEventsUsed(game)
	lineupT1 = getLineups(eventNums, game, t2, t1, tp2, default1, starters)
	lineupT2 = getLineups(eventNums, game, t1, t2, tp1, default1, starters)
	lineup = []
	#lineup += [['time_s', 'time_e', 'event_s', 'event_e', 'player_1', 'player_2', 'player_3', 'player_4', 'player_5', 'team_id', 'game_id', 'period']]
	for line in lineupT1:
		lineup += [line]
	for line in lineupT2:
		lineup += [line]
	subs = ftSubNums(game, eventNums)
	performance = createTotals(lineup, possessions, game, eventNums, points)
	perf2 = removeDupes(performance)
	finalPerformance = []
	finalPerformance += [['team_id', 'player_id', 'game_id', 'offense', 'defense', 'offPos', 'defPos', 'totalPoss']]
	for row in perf2:
		finalPerformance += [row]
	game = displayGame(game)
	writeCSV('lineup.csv', finalPerformance)
	writeCSV('game.csv', game)

if __name__ == "__main__":
	main()
