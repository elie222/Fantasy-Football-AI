import urllib
from bs4 import BeautifulSoup
import json
import glob
import sys
from prettytable import PrettyTable
import math

'''
Usage:
python calculatePlayerStats.py <player position> <no of games> <discount factor> <sort by>
player position: 1-4 (gk to striker). 5 - all
no of games: integer
discount factor: double
sort by: 'EP' or 'Value'
'''
#TODO - yellow and red cards. penalty saves?

playerPosition = sys.argv[1]
noOfGameweeks = int(sys.argv[2])
discountFactor = float(sys.argv[3])
sortBy = sys.argv[4]

##root = '8_2_2013'#TODO change depending on date
root = '26_3_2013'
tableFile = 'tableHomeAndAway.html'

teamNames = {}
teamNames['Manchester United'] = 'Man Utd'
teamNames['Manchester City'] = 'Man City'
teamNames['Tottenham Hotspur'] = 'Tottenham'
teamNames['Chelsea'] = 'Chelsea'
teamNames['Everton'] = 'Everton'
teamNames['Arsenal'] = 'Arsenal'
teamNames['West Bromwich Albion'] = 'West Brom'
teamNames['Liverpool'] = 'Liverpool'
teamNames['Swansea City'] = 'Swansea'
teamNames['Stoke City'] = 'Stoke City'
teamNames['West Ham United'] = 'West Ham'
teamNames['Norwich City'] = 'Norwich'
teamNames['Fulham'] = 'Fulham'
teamNames['Sunderland'] = 'Sunderland'
teamNames['Newcastle United'] = 'Newcastle'
teamNames['Aston Villa'] = 'Aston Villa'
teamNames['Southampton'] = 'Southampton'
teamNames['Wigan Athletic'] = 'Wigan'
teamNames['Reading'] = 'Reading'
teamNames['Queens Park Rangers'] = 'QPR'

fullTable = []

#htmlTable = urllib.urlopen("http://www.premierleague.com/en-gb/matchday/league-table.html?season=2012-2013&month=JULY&timelineView=date&toDate=1357171199999&tableView=HOME_VS_AWAY").read()
htmlTable = open(root + '/' + tableFile, 'r')
soup = BeautifulSoup(htmlTable)
htmlTable.close()

teams = soup.find_all("td", class_="club-names")
for team in teams:
    teamData = []
    teamData.append(team.get_text())
    nextRow = team.find_next_sibling()
    while (nextRow is not None):
        teamData.append(nextRow.get_text())
        nextRow = nextRow.find_next_sibling()
    fullTable.append(teamData)

#print fullTable

#GF Home
#calculate average goals for at home
total = 0
for teamData in fullTable:
    total += float(teamData[5])
    
avgGoalsForHome = total/20
#print avgGoalsForHome

#percentage above/below average:
for teamData in fullTable:
    #print teamData[0]
    teamData.append(int(teamData[5])/avgGoalsForHome)
    #print teamData[19]


#GA Home
#calculate average goals against at home
total = 0
for teamData in fullTable:
    total += float(teamData[6])
    
avgGoalsAgainstHome = total/20
#print avgGoalsAgainstHome

#percentage above/below average:
for teamData in fullTable:
    #print teamData[0]
    teamData.append(int(teamData[6])/avgGoalsForHome)
    #print teamData[20]


#GF Away
#percentage above/below average:
for teamData in fullTable:
##    print teamData[0]
    teamData.append(int(teamData[13])/avgGoalsAgainstHome)
##    print teamData[21]

#GA Away
#percentage above/below average:
for teamData in fullTable:
    #print teamData[0]
    teamData.append(int(teamData[14])/avgGoalsForHome)
    #print teamData[22]

avgGoals = avgGoalsAgainstHome+((avgGoalsForHome-avgGoalsAgainstHome)/2)
homeAdv = avgGoalsForHome/avgGoals
awayDisadv = avgGoalsAgainstHome/avgGoals

print 'home advantage: ' + str(homeAdv)
print 'away disadvantage: ' + str(awayDisadv)
print 'finished with pl table'

'''
teamData[0] = team name

--Home
teamData[1] = played
teamData[2] = won
teamData[3] = drawn
teamData[4] = lost
teamData[5] = GF
teamData[6] = GA
teamData[7] = GD
teamData[8] = points

--Away
teamData[9] = played
teamData[10] = won
teamData[11] = drawn
teamData[12] = lost
teamData[13] = GF
teamData[14] = GA
teamData[15] = GD
teamData[16] = points

--Overall
teamData[17] = GD
teamData[18] = points

--Data I added:
--Home
teamData[19] = GF above/below average (fraction)
teamData[20] = GA above/below average (fraction)
--Away
teamData[21] = GF above/below average (fraction)
teamData[22] = GA above/below average (fraction)
'''

#==========================================
def calculateDefensivePPG(player):
    gamesPlayed = 0
    cleanSheets = 0
    goalsConceded = 0
    bonusPoints = 0
    saves = 0

    bonusValue = 1
    if player['element_type_id'] == 3:
        bonusValue = 0

    pointsForCS = 0
    pointsForGoalConceded = 0
    pointsForSave = 0.25
    if player['element_type_id'] == 1 or player['element_type_id'] == 2:
        pointsForCS = 4
        pointsForGoalConceded = -0.3
    elif player['element_type_id'] == 3:
        pointsForCS = 1

    for fixture in player['fixture_history']['all']:
        if fixture[3]>0:
            gamesPlayed += 1
        else:
            continue
        cleanSheets += fixture[6]
        goalsConceded += fixture[7]
        bonusPoints += fixture[14]
        saves += fixture[13]

    if gamesPlayed == 0:
        return 0

    defensivePoints = (cleanSheets*pointsForCS)+(goalsConceded*pointsForGoalConceded)+(saves*pointsForSave)+(bonusPoints*bonusValue)

##    if player['element_type_id'] == 1:
##        print player['web_name'], float(defensivePoints)/gamesPlayed
    
    return float(defensivePoints)/gamesPlayed

def calculateAttackingPPG(player):
    gamesPlayed = 0
    goalsScored = 0
    assists = 0
    bonusPoints = 0

    bonusValue = 1
    if player['element_type_id'] == 2:
        bonusValue = 0
    
    pointsPerGoal = 0
    if player['element_type_id'] == 2:
        pointsPerGoal = 6
    elif player['element_type_id'] == 3:
        pointsPerGoal = 5
    elif player['element_type_id'] == 4:
        pointsPerGoal = 4

    for fixture in player['fixture_history']['all']:
        if fixture[3]>0:
            gamesPlayed += 1
        else:
            continue
        goalsScored += fixture[4]
        assists += fixture[5]
        bonusPoints += fixture[14]

    if gamesPlayed == 0:
        return 0
        
    attackingPoints = (goalsScored*pointsPerGoal)+(assists*3)+(bonusPoints*bonusValue)
    return float(attackingPoints)/gamesPlayed

def calculateCardsPPG(player):
    YELLOW_CARD = -1
    RED_CARD = -3

    noOfYellowCards = 0
    noOfRedCards = 0
    gamesPlayed = 0

    for fixture in player['fixture_history']['all']:
        if fixture[3]>0:
            gamesPlayed += 1
        else:
            continue
        noOfYellowCards += fixture[11]
        noOfRedCards += fixture[12]

    if gamesPlayed == 0:
        return 0

    return float((noOfYellowCards*YELLOW_CARD) + (noOfRedCards*RED_CARD))/gamesPlayed


def calculateOppAttackingStrength(opponent, place):
    oppStrength = 0
    for teamData in fullTable:
        if teamNames[teamData[0]] == opponent:
            if place == 'H':
                oppStrength = teamData[21]
                oppStrength = oppStrength*awayDisadv
            elif place == 'A':
                oppStrength = teamData[19]
                oppStrength = oppStrength*homeAdv
##    print opponent, place, oppStrength
    return oppStrength

def calculateOppDefensiveStrength(opponent, place):
    oppStrength = 0
    for teamData in fullTable:
        if teamNames[teamData[0]] == opponent:
            if place == 'H':
                oppStrength = teamData[22]
                oppStrength = oppStrength*awayDisadv
            elif place == 'A':
                oppStrength = teamData[20]
                oppStrength = oppStrength*homeAdv
##    print opponent, place, oppStrength
    return oppStrength

def calculateExpectedPlayerScore(player, opponent, place):
    pointsForPlaying = 2
    #for debugging
##    if player['web_name'] == 'Walcott':
##        print 'Walcott:'
##        print 'EP:', pointsForPlaying+((calculateDefensivePPG(player)/calculateOppAttackingStrength(opponent, place)) + (calculateAttackingPPG(player)*calculateOppDefensiveStrength(opponent, place)))
##        print 'defensive PPG:', calculateDefensivePPG(player)
##        print 'attacking PPG:', calculateAttackingPPG(player)
##        print 'opp attack strength: ', calculateOppAttackingStrength(opponent, place)
##        print 'opp defensive strength: ', calculateOppDefensiveStrength(opponent, place)
    if player['element_type_id'] == 1:
        return pointsForPlaying+(calculateDefensivePPG(player)/calculateOppAttackingStrength(opponent, place)) + calculateCardsPPG(player)
    elif player['element_type_id'] == 2 or player['element_type_id'] == 3:
        return pointsForPlaying+((calculateDefensivePPG(player)/calculateOppAttackingStrength(opponent, place)) + (calculateAttackingPPG(player)*calculateOppDefensiveStrength(opponent, place))) + calculateCardsPPG(player)
    elif player['element_type_id'] == 4:
        return pointsForPlaying+(calculateAttackingPPG(player)*calculateOppDefensiveStrength(opponent, place)) + calculateCardsPPG(player)

def calculatePlayerExpScore(player, discountFactor=1):
    #TODO. points per week not working when a player has a DGW.
    expectedScore = 0
    pointsPerWeek = []#a table containing the no. of points a player is expected to get over each of the next noOfGameweeks
    
    #print player['id']
    #print player['web_name']
    
    #TODO discount factor not working anymore for double gameweeks.
    for i in range(38):
        nextMatch = player['fixtures']['all'][i][2]
        #TODO this won't work at the beginning of the season when GW numbers are only 1 digit
        if int(player['fixtures']['all'][i][1][-2:]) == endGameweek:
            break
        if nextMatch == '-':
            pointsPerWeek.append(0)
            continue
        opponent = nextMatch[:-4]
        place = nextMatch[-2]
        pointsPerWeek.append(calculateExpectedPlayerScore(player, opponent, place))

##        if player['element_type_id'] == 1:
##            print player['web_name'], pointsPerWeek[i]
        
        expectedScore += math.pow(discountFactor,i)*pointsPerWeek[i]
    #if player['status'] == 'd':
    #    return expectedScore/2#this should really be times 0.75, 0.5 or 0.25 depending on the situation
    if player['status'] == 'u' or player['status'] == 'i' or player['status'] == 'n' or player['status'] == 's':
       expectedScore = 0

    return expectedScore, pointsPerWeek

def calculateAppearanceStats(player):
    #TODO work out stats for last 6 games.
    
    maxPossibleMinsPlayed = 0
    totalMinsPlayed = 0

    #can get real statistics for this stuff off the internet, but that'll be a bit of a hassle.
    noOfGamesNotPlayedIn = 0
    noOfGamesStarted = 0 # assuming that the no. of games player has started is all games in which he has played <45 mins
    noOfGamesSubbedIn = 0 # assuming player has played >=45 mins in a game.
    
    for fixture in player['fixture_history']['all']:
        maxPossibleMinsPlayed += 90
        totalMinsPlayed += fixture[3] #fixture[3] is the number of minutes played in the fixture.
        if fixture[3] == 0:
            noOfGamesNotPlayedIn += 1
        elif fixture[3] > 45:
            noOfGamesStarted += 1
        elif fixture[3] <= 45:
            noOfGamesSubbedIn += 1

    minutesPlayedInLast6 = 0

    for fixture in player['fixture_history']['all'][-6:]:
        minutesPlayedInLast6 += fixture[3]

    result = {}

    result['maxPossibleMinsPlayed'] = maxPossibleMinsPlayed
    result['totalMinsPlayed'] = totalMinsPlayed

    result['gamesStarted'] = noOfGamesStarted
    result['gamesSubbedIn'] = noOfGamesSubbedIn
    result['gamesNotPlayedIn'] = noOfGamesNotPlayedIn

    result['minutesPlayedInLast6'] = minutesPlayedInLast6
    
    return result

#======================================================
# CALCULATING PLAYER SCORES
#======================================================

goalkeepers = []
defenders = []
midfielders = []
strikers = []
allPlayers = []

playerFiles = glob.glob(root + '/*')
playerFiles.remove(root + '/' + tableFile)

jsonPlayer = open(root + '/1', 'r')#TODO change this line
htmlPlayer = jsonPlayer.read()
player = json.loads(htmlPlayer)
jsonPlayer.close()
#TODO this won't work for the beginning of the season where the gameweek no. is 1 digit instead of 2
startGameweek = int(player['fixtures']['all'][0][1][-2:])
#endGameweek is not included the calculating of the scores.
endGameweek = startGameweek + noOfGameweeks;

for playerFile in playerFiles:
    jsonPlayer = open(playerFile, 'r')
    htmlPlayer = jsonPlayer.read()
    try:
        player = json.loads(htmlPlayer)
    except:
        print 'there was an error for file: ' + playerFile
        print "Error: ", sys.exc_info()[0]
        jsonPlayer.close()
        continue
    jsonPlayer.close()

    #maybe comment this out. won't be able to see new players
    if player['total_points'] < 20:
        continue
    
    #print player['web_name']
    #print player['team_name']
    #print player['now_cost']
    #print player['total_points']
    #print player['points_per_game']
    #print player['status']
    #print player['element_type_id']#position 1-4

    expectedPoints, pointsPerWeek = calculatePlayerExpScore(player, discountFactor)

    playerInfo = []
    playerInfo.append(player['web_name'])#[0]
    playerInfo.append(player['team_name'])#[1]
    playerInfo.append(float(player['now_cost'])/10)#[2]
    playerInfo.append(player['total_points'])#[3]
    playerInfo.append(player['status'])#[4]
    playerInfo.append(round(expectedPoints,1))#[5]
    playerInfo.append(round(expectedPoints/(float(player['now_cost'])/10),1))#[6]
    playerInfo.append(player['element_type_id'])#[7]
    playerInfo.append(calculateAppearanceStats(player))#[8]
    playerInfo.append(pointsPerWeek)#[9]

    if player['element_type_id'] == 1:
        goalkeepers.append(playerInfo)
##        if expectedPoints > 12: #want an an average of at least 2 points per week. assumes 6 weeks
##            goalkeepersPrices.append(int(player['now_cost']))
##            goalkeepersValues.append(int(round(expectedPoints,1)))
##            goalkeepersNames.append(player['web_name'])
    elif player['element_type_id'] == 2:
        defenders.append(playerInfo)
    elif player['element_type_id'] == 3:
        midfielders.append(playerInfo)
    elif player['element_type_id'] == 4:
        strikers.append(playerInfo)

#======================================================
# PRINTING RESULTS
#======================================================

allPlayers.extend(goalkeepers)
allPlayers.extend(defenders)
allPlayers.extend(midfielders)
allPlayers.extend(strikers)

from operator import itemgetter
goalkeepers = sorted(goalkeepers, key=itemgetter(6), reverse=True)
defenders = sorted(defenders, key=itemgetter(6), reverse=True)
midfielders = sorted(midfielders, key=itemgetter(6), reverse=True)
strikers = sorted(strikers, key=itemgetter(6), reverse=True)

table = PrettyTable(['Name','Team','Cost','Points','Status','EP','Value','Position'], sortby=sortBy)
table.align['Name'] = '1'

if (playerPosition == '1'):
    for goalkeeper in goalkeepers:
        row = goalkeeper[:8]
        table.add_row(row)
elif (playerPosition == '2'):
    for defender in defenders:
        row = defender[:8]
        table.add_row(row)
elif (playerPosition == '3'):
    for midfielder in midfielders:
        row = midfielder[:8]
        table.add_row(row)
elif (playerPosition == '4'):
    for striker in strikers:
        row = striker[:8]
        table.add_row(row)
elif (playerPosition == '5'):
    for player in allPlayers:
        row = player[:8]
        table.add_row(row)
else:
    print 'invalid arg. Got:'
    print playerPosition

print table

#======================================================
# CHOOSING A TEAM
#======================================================

#DONE work out the probability of a player starting/being subbed off.
#DONE work out ways of not choosing players that are unlikely to start or are injured.
#TODO add constraints to stop 3 players being picked from the same team. i think the best is to pick the best team and then remove players that break constraints
#WORKING ON THIS choose keepers by picking a good rotating policy.
#TODO make sure to have the highest scoring in the team. even if they're bad value (eg. RVP). these players are important since they can be captained and score double which improves their value a lot.
#TODO probably first pick the 3 highest scoring players for the next 6 weeks, choose the 2 keepers we want and then fill in the rest of the team
#TODO work a plan for dealing with subs. eg. would be good to have some super cheap subs that will probs never play for us anyway.
#TODO pick the best lineup for the following week
#TODO work out when it is worth transferring players and taking a hit on a transfer
#TODO need to make sure we have at least one very cheap def since he'll probs never play anyway

def combineToOne(gks,defs,mids,strs):
    team = []
    team.extend(gks)
    team.extend(defs)
    team.extend(mids)
    team.extend(strs)
    return team

def printTeam(players):
    print '\nPRINTING chosenTeam'
    table = PrettyTable(['Name','Team','Cost','Points','Status','EP','Value', 'Position'])
    table.align['Name'] = '1'

    for player in players:
        row = player[:8]
        table.add_row(row)
        
    print table
    print 'Team Cost:', calcTeamCost(players)
    print 'Expected points over the next six weeks:', calcTeamEP(players)

def calcTeamCost(players):
    totalCost = 0
    for player in players:
        totalCost += player[2]
    return totalCost

def calcTeamEP(players):
    ep = 0
    for player in players:
        ep += player[5]
    return ep

def removeLowEPs(posList, chosenPlayersInPos):
    minEP = 1000
    for player in chosenPlayersInPos:
        if player[5] < minEP:
            minEP = player[5]

    posList = [p for p in posList if p[5]>minEP]
            
    return posList

def removeUnlikelyStarters(players):
    #this could definitely remove players we're interested in. maybe change to only look at recent games
    
    #TODO can do more in this function. eg. removing players that have played 1 game all season, even if it was 90mins they played
    result = [p for p in players if p[8]['gamesSubbedIn']*2 < p[8]['gamesStarted']]
    result = [p for p in result if p[8]['minutesPlayedInLast6'] > 360]#this could have bad affects on players coming back from injuries/suspensions
    return result

def findWorstEPPlayer(players, checkGK=True, checkDef=True, checkMid=True, checkStr=True, position=5):
    worstEPPlayer = None

    for player in players:
        check = False
        if player[7] == 1 and (position == 1 or position == 5):
            check = checkGK
        elif player[7] == 2 and (position == 2 or position == 5):
            check = checkDef
        elif player[7] == 3 and (position == 3 or position == 5):
            check = checkMid
        elif player[7] == 4 and (position == 4 or position == 5):
            check = checkStr
        if check:
            if not player[10]:
                if worstEPPlayer is None:
                    worstEPPlayer = player
                elif player[5] < worstEPPlayer[5]:
                    worstEPPlayer = player

    return worstEPPlayer

def findBestEPPlayer(players):
    bestPlayer = None
    
    for p in players:
        if p[0] == 'Van Perise':
            print 'FOUND RVP'
        if bestPlayer == None:
            bestPlayer = p
        elif p[5]>bestPlayer[5]:
            bestPlayer = p

    return bestPlayer

#old is the player we are replacing. return None if we don't find a replacement better than him
#ie. if there is no player with a better EP than old.
def findBestValuePlayerIn(posList, old):
    if len(posList) == 0:
        return None
    if not old[7] == posList[0][7]:
        print 'ERROR in function findBestValuePlayerIn(posList, old)'
        return None
    
    bestValuePlayer = None

    for player in posList:
        if player[5] > old[5]:
            if bestValuePlayer == None:
                bestValuePlayer = player
            elif player[6] > bestValuePlayer[6]: 
                bestValuePlayer = player

    return bestValuePlayer

def replacePlayer(old, new, players):
    #to do check to make sure old and new player play in the same pos. (just to be safe)
    if old is None or new is None:
        return players

    if new in players:
        return players

    if old not in players:
        return players
    
    players.remove(old)
    players.append(new)
    return players

#before calling this function, remove all gks we def. don't want
def calcGkPairs(gks):
    gkPairs = []
    for gk1 in gks:
        if gk1[5] == 0:
            continue
        for gk2 in gks:
            if gk2[5] == 0:
                continue
            if not gk1 == gk2 and gk1[0]<gk2[0]:
                gkPairs.append([gk1,gk2])

    finalGkPairs = []
    
    for gkPair in gkPairs:
        pairScore = 0
        
        #the correct code is commented out, but due to a bug in CalculatePlayerExpScore it doesn't work
        #for i in range(len(gkPair[0][9])):
        #the next line is wrong
        for i in range(6):
            if gkPair[0][9][i] > gkPair[1][9][i]:
                pairScore += gkPair[0][9][i]
            else:
                pairScore += gkPair[1][9][i]

        gkPairDict = {}
        gkPairDict['gkPair'] = gkPair
        gkPairDict['score'] = pairScore
        gkPairDict['price'] = gkPair[0][2] + gkPair[1][2]
        gkPairDict['value'] = gkPairDict['score']/gkPairDict['price']

        finalGkPairs.append(gkPairDict)
        
    return sorted(finalGkPairs,key=itemgetter('value'), reverse=True)

#adds an option whether this player can be removed from the chosen team
def addDontTouchPlayerOptionTo(players):
    res = []
    for p in players:
        newP = p
        newP.append(False)# == newP[10]
        res.append(newP)

    return res

moneyRemaining = 105

print len(strikers)
print '========STRIKERS before=========\n'
for s in strikers:
    print s[0]
print ''

#removing unlikely starters
goalkeepers = removeUnlikelyStarters(goalkeepers)
defenders = removeUnlikelyStarters(defenders)
midfielders = removeUnlikelyStarters(midfielders)
strikers = removeUnlikelyStarters(strikers)
##print len(goalkeepers)
##print len(defenders)
##print len(midfielders)
print len(strikers)
print '========STRIKERS after=========\n'
for s in strikers:
    print s[0]
print ''

goalkeepers = addDontTouchPlayerOptionTo(goalkeepers)
defenders = addDontTouchPlayerOptionTo(defenders)
midfielders = addDontTouchPlayerOptionTo(midfielders)
strikers = addDontTouchPlayerOptionTo(strikers)

gkPairs = calcGkPairs(goalkeepers)

#picking best value team
##chosenGoalkeepers = goalkeepers[:2]
chosenGoalkeepers = []
chosenGoalkeepers.append(gkPairs[0]['gkPair'][0])
chosenGoalkeepers.append(gkPairs[0]['gkPair'][1])

#print chosenGoalkeepers

chosenDefenders = []
bestValDef = defenders[0]
bestValDef[10] = True
secondBestValDef = defenders[1]
secondBestValDef[10] = True
chosenDefenders.append(bestValDef)
chosenDefenders.append(secondBestValDef)
chosenDefenders.append(defenders[2])
chosenDefenders.append(defenders[3])
chosenDefenders.append(defenders[4])
chosenMidfielders = midfielders[:5]
chosenStrikers = strikers[:3]

chosenTeam = combineToOne(chosenGoalkeepers,chosenDefenders,chosenMidfielders,chosenStrikers)

#choose 5 highest ep players and put them into the team and don't remove them ever
for i in range(5):
    bestEPPlayer = findBestEPPlayer(combineToOne(goalkeepers,defenders,midfielders,strikers))
    print bestEPPlayer[0]
    if bestEPPlayer[7]==1:
        goalkeepers.remove(bestEPPlayer)
    if bestEPPlayer[7]==2:
        defenders.remove(bestEPPlayer)
    if bestEPPlayer[7]==3:
        midfielders.remove(bestEPPlayer)
    if bestEPPlayer[7]==4:
        strikers.remove(bestEPPlayer)
    bestEPPlayer[10] = True #don't remove this player from the chosen team
    worstEPPlayer = findWorstEPPlayer(chosenTeam, position=bestEPPlayer[7])
##    print bestEPPlayer[0]
##    print worstEPPlayer[0]
    chosenTeam = replacePlayer(worstEPPlayer, bestEPPlayer, chosenTeam)


teamCost = calcTeamCost(chosenTeam)
moneyRemaining -= teamCost

#printTeam(chosenTeam)

#improve team. use spare cash that we have.

checkGKPairs = False
checkDef = True
checkMid = True
checkStr = True

if len(gkPairs) == 0:
    checkGKPairs = False
if len(defenders) == 0:
    checkDef = False
if len(midfielders) == 0:
    checkMid = False
if len(strikers) == 0:
    checkStr = False

while not len(goalkeepers)+len(defenders)+len(midfielders)+len(strikers) == 0:    
    #remove all players that have a lower EP than the lowest EP (in each position)
    #goalkeepers have to be done differently. replace with pairs.
    #goalkeepers = [gk for gk in goalkeepers if gk not in chosenGoalkeepers]
    defenders = [d for d in defenders if d not in chosenDefenders]
    midfielders = [m for m in midfielders if m not in chosenMidfielders]
    strikers = [s for s in strikers if s not in chosenStrikers]

    goalkeepers = removeLowEPs(goalkeepers, chosenGoalkeepers)
    defenders = removeLowEPs(defenders, chosenDefenders)
    midfielders = removeLowEPs(midfielders, chosenMidfielders)
    strikers = removeLowEPs(strikers, chosenStrikers)

    if len(gkPairs) == 0:
        checkGKPairs = False
    if len(defenders) == 0:
        checkDef = False
    if len(midfielders) == 0:
        checkMid = False
    if len(strikers) == 0:
        checkStr = False

    worstEPP = findWorstEPPlayer(chosenTeam, checkGKPairs, checkDef, checkMid, checkStr)

    if worstEPP is None:
        break

##    if worstEPP[7] == 1:
##        bestReplacement = findBestValuePlayerIn(goalkeepers, worstEPP)
##        if bestReplacement == None:
##            goalkeepers = []
##            continue
##        if bestReplacement[2] - worstEPP[2] <= moneyRemaining:
##            moneyRemaining -= (bestReplacement[2] - worstEPP[2])
##            chosenTeam = replacePlayer(worstEPP, bestReplacement, chosenTeam)
##        goalkeepers.remove(bestReplacement)
            #do again and again until we find a replacement or until the list is empty
            #when list is empty, check to see if we can make replacements in other positions
            #when all lists are empty, we have our team
    if worstEPP[7] == 2:
        bestReplacement = findBestValuePlayerIn(defenders, worstEPP)
        if bestReplacement == None:
            defenders = []
            continue
        if bestReplacement[2] - worstEPP[2] <= moneyRemaining:
            moneyRemaining -= (bestReplacement[2] - worstEPP[2])
            chosenTeam = replacePlayer(worstEPP, bestReplacement, chosenTeam)
        defenders.remove(bestReplacement)
    elif worstEPP[7] == 3:
        bestReplacement = findBestValuePlayerIn(midfielders, worstEPP)
        if bestReplacement == None:
            midfielders = []
            continue
        if bestReplacement[2] - worstEPP[2] <= moneyRemaining:
            moneyRemaining -= (bestReplacement[2] - worstEPP[2])
            chosenTeam = replacePlayer(worstEPP, bestReplacement, chosenTeam)
        midfielders.remove(bestReplacement)
    elif worstEPP[7] == 4:
        bestReplacement = findBestValuePlayerIn(strikers, worstEPP)
        if bestReplacement == None:
            strikers = []
            continue
        if bestReplacement[2] - worstEPP[2] <= moneyRemaining:
            moneyRemaining -= (bestReplacement[2] - worstEPP[2])
            chosenTeam = replacePlayer(worstEPP, bestReplacement, chosenTeam)
        strikers.remove(bestReplacement)

printTeam(chosenTeam)



##team1 = ['Mignolet', 'Bunn', 'Rafael', 'Nastasic', 'Azpilicueta', 'Naughton', 'Davies', 'Mata', 'Walcott', 'Fellaini', 'Dempsey', 'Michu', 'Van Persie', 'Fletcher', 'Pogrebnyak']
##team2 = ['Mignolet', 'Bunn', 'Rafael', 'Zabaleta', 'Azpilicueta', 'Harte', 'Davies', 'Mata', 'Walcott', 'Fellaini', 'Dempsey', 'Michu', 'Van Persie', 'Fletcher', 'Pogrebnyak']
##team3 = []
##team1IDs = [380, 609, 200, 596, 574, 441, 575, 83, 15, 105, 132, 537, 26, 573]
##team2IDs = [380, 609, 200, 175, 574, 313, 575, 83, 15, 105, 132, 537, 26, 573]
##team3IDs = []
##team1Score = 0
##team2Score = 0
##team3Score = 0
##
###team 1
##for playerID in team1IDs:
##    jsonPlayer = open(root + '/' + str(playerID), 'r')
##    htmlPlayer = jsonPlayer.read()
##    try:
##        player = json.loads(htmlPlayer)
##    except:
##        print 'there was an error for file: ' + playerFile
##        print "Error: ", sys.exc_info()[0]
##        jsonPlayer.close()
##        continue
##    jsonPlayer.close()
##    
##    #print player['web_name']
##
##    expectedPoints = calculatePlayerExpScore(player, int(sys.argv[2]), float(sys.argv[3]))
##
##    playerInfo = []
##    playerInfo.append(player['web_name'])
##    playerInfo.append(player['team_name'])
##    playerInfo.append(float(player['now_cost'])/10)
##    playerInfo.append(player['total_points'])
##    playerInfo.append(player['status'])
##    playerInfo.append(expectedPoints)
##    playerInfo.append(expectedPoints/(float(player['now_cost'])/10))
##    team1Score += expectedPoints
##print team1Score
##
###team 2
##for playerID in team2IDs:
##    jsonPlayer = open(root + '/' + str(playerID), 'r')
##    htmlPlayer = jsonPlayer.read()
##    try:
##        player = json.loads(htmlPlayer)
##    except:
##        print 'there was an error for file: ' + playerFile
##        print "Error: ", sys.exc_info()[0]
##        jsonPlayer.close()
##        continue
##    jsonPlayer.close()
##    
##    #print player['web_name']
##
##    expectedPoints = calculatePlayerExpScore(player, int(sys.argv[2]), float(sys.argv[3]))
##
##    playerInfo = []
##    playerInfo.append(player['web_name'])
##    playerInfo.append(player['team_name'])
##    playerInfo.append(float(player['now_cost'])/10)
##    playerInfo.append(player['total_points'])
##    playerInfo.append(player['status'])
##    playerInfo.append(expectedPoints)
##    playerInfo.append(expectedPoints/(float(player['now_cost'])/10))
##    team2Score += expectedPoints
##print team2Score



