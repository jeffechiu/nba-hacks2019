openCSV - opens a CSV file in a dictreader format in Python, returns every row of the DictReader as an array

getGames - takes an array of dictreader elements, and gets all game IDS returned into an array

parseGames - gets all dictReader elements of one game, returned in array

getTeamIDS - gets the 2 team IDS of a game

getTeamPlayerIDS - gets the player IDS of the team formats

sortEventNums - sorts the event numbers of a game

modifyGame - changes around the event numbers in a game to account for how free throws and technical fouls should be calculated

getPossessions - gets a total of all possessions in a game in event num format (start of possession num to end of possession num) in an array

getOffPos - getPossessions but for offensive possessions

getDefPos - getPossessinos but for defensive possessions

getNumPossessions - gets total number of possessions between 2 event nums

getOffPossessions - getNumPossessions but for offensive possessions

getDefPossessions - getNumPossessions but for defensive possessions

getPoints - gets all points in terms of eventNums returned as an 2d array where elements
are stored as [point total, event num, team that scored]

getOffDef - get points scored and points allowed given a certain range of event nums

getLineUp - gets all lineups used in a game

ftSubNums - gets all event nums of when substitutions were made

createTotals and removeDupes - creates final

writeCSV - turns written dictreader into csv file
