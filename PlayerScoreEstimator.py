from bs4 import BeautifulSoup
import json

# TODO change this
TABLE_FILENAME = 'TEST_TABLE.html'
TEST_PLAYER_FILENAME = 'TEST_PLAYER'

HOME_ADV = 1.14
AWAY_DISADV = 0.86

CS_DEF_POINTS = 4
CS_MID_POINTS = 1
ASSIST_POINTS = 3
GOAL_DEF_POINTS = 6
GOAL_MID_POINTS = 5
GOAL_ATT_POINTS = 4
YELLOW_POINTS = -1
RED_POINTS = -3
BONUS_POINTS = 1

SAVE_POINTS = 0.25
GOAL_CONC_DEF_POINTS = -0.3

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


class PlayerScoreEstimator:
    def __init__(self, tableFilename=TABLE_FILENAME):
        self.createTable(tableFilename)

    def estimateScore(self,player,opponentName,location):
        # opponentTeam = self.table[player['team_name']]
        opponentTeam = self.table[opponentName]
        oppAttStrength = 0
        oppDefStrength = 0
        locAdv = 0

        if location == 'H':
            oppAttStrength = float(opponentTeam['awayGF'])/self.table.avgAwayGF
            oppDefStrength = float(opponentTeam['awayGA'])/self.table.avgAwayGA
            locAdv = HOME_ADV
        elif location == 'A':
            oppAttStrength = float(opponentTeam['homeGF'])/self.table.avgHomeGF
            oppDefStrength = float(opponentTeam['homeGA'])/self.table.avgHomeGA
            locAdv = AWAY_DISADV
        else:
            raise

        return self.calcMiscPPG(player)+(locAdv*((self.calcDefPPG(player)/oppAttStrength)+(self.calcAttPPG(player)*oppDefStrength)))

    def calcDefPPG(self,player):
        gamesPlayed = 0
        points = 0
        csPoints = 0
        gcPoints = 0
        bonusPoints = 0

        if player['element_type_id'] == 1 or player['element_type_id'] == 2:
            csPoints = CS_DEF_POINTS
            gcPoints = GOAL_CONC_DEF_POINTS
            bonusPoints = BONUS_POINTS
        elif player['element_type_id'] == 3:
            csPoints = CS_MID_POINTS

        fixture = None
        for fixtureArray in player['fixture_history']['all']:
            fixture = Fixture(fixtureArray)
            if fixture['minsPlayed'] == 0:
                continue
            gamesPlayed += 1
            points += (fixture['cleanSheets']*csPoints)
            points += (fixture['saves']*SAVE_POINTS)
            points += (fixture['goalsConceded']*gcPoints)
            points += (fixture['bonus']*bonusPoints)

        if gamesPlayed == 0:
            return 0
        else:
            return float(points)/gamesPlayed

    def calcAttPPG(self,player):
        gamesPlayed = 0
        points = 0
        goalPoints = 0
        bonusPoints = 0

        if player['element_type_id'] == 2:
            goalPoints = GOAL_DEF_POINTS
        elif player['element_type_id'] == 3:
            goalPoints = GOAL_MID_POINTS
            bonusPoints = BONUS_POINTS
        elif player['element_type_id'] == 4:
            goalPoints = GOAL_ATT_POINTS
            bonusPoints = BONUS_POINTS

        fixture = None
        for fixtureArray in player['fixture_history']['all']:
            fixture = Fixture(fixtureArray)
            if fixture['minsPlayed'] == 0:
                continue
            gamesPlayed += 1
            points += (fixture['goalsScored']*goalPoints)
            points += (fixture['assists']*ASSIST_POINTS)
            points += (fixture['bonus']*bonusPoints)

        if gamesPlayed == 0:
            return 0
        else:
            return float(points)/gamesPlayed

    def calcMiscPPG(self,player):
        gamesPlayed = 0
        points = 0

        fixture = None
        for fixtureArray in player['fixture_history']['all']:
            fixture = Fixture(fixtureArray)
            if fixture['minsPlayed'] == 0:
                continue
            gamesPlayed += 1
            points += (fixture['yellowCards']*YELLOW_POINTS)
            points += (fixture['redCards']*RED_POINTS)
            if fixture['minsPlayed'] >= 60:
                points += 2
            else:
                points += 1

        if gamesPlayed == 0:
            return 0
        else:
            return float(points)/gamesPlayed

    def createTable(self, filename):
        html = open(filename, 'r')
        soup = BeautifulSoup(html)
        html.close()

        self.table = Table(0)#TODO

        teams = soup.find_all("td", class_="club-names")
        for team in teams:
            teamData = []
            teamData.append(team.get_text())
            nextRow = team.find_next_sibling()
            while (nextRow is not None):
                teamData.append(nextRow.get_text())
                nextRow = nextRow.find_next_sibling()

            self.table.addTeam(Team(teamData))

        self.table.initAverages()

class Table:
    def __init__(self, gameweek):
        self.gameweek = gameweek
        self.data = {}

    def initAverages(self):
        self.avgHomeGF = self.calcAverage('homeGF')
        self.avgHomeGA = self.calcAverage('homeGA')
        self.avgAwayGF = self.calcAverage('awayGF')
        self.avgAwayGA = self.calcAverage('awayGA')

    def calcAverage(self, avgType):
        goals = 0
        for team in self.data:
            goals += self[team][avgType]
        return goals/len(self.data)

    def addTeam(self, team):
        self[team.teamName] = team

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

class Team:
    def __init__(self, teamData):
        self.teamName = teamData[0]
        self.data = {}

        self.data['homePlayed'] = int(teamData[1])
        self.data['homeWon'] = int(teamData[2])
        self.data['homeDrawn'] = int(teamData[3])
        self.data['homeLost'] = int(teamData[4])
        self.data['homeGF'] = int(teamData[5])
        self.data['homeGA'] = int(teamData[6])
        self.data['homeGD'] = int(teamData[7])
        self.data['homePoints'] = int(teamData[8])

        self.data['awayPlayed'] = int(teamData[9])
        self.data['awayWon'] = int(teamData[10])
        self.data['awayDrawn'] = int(teamData[11])
        self.data['awayLost'] = int(teamData[12])
        self.data['awayGF'] = int(teamData[13])
        self.data['awayGA'] = int(teamData[14])
        self.data['awayGD'] = int(teamData[15])
        self.data['awayPoints'] = int(teamData[16])

        self.data['overallGD'] = int(teamData[17])
        self.data['overallPoints'] = int(teamData[18])

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

class Player:
    def __init__(self, filename):
        f = open(filename,'r')
        self.data = json.loads(f.read())
        f.close()

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

class Fixture:
    def __init__(self, array):
        self.data = {}

        self.data['date'] = array[0]
        self.data['gameweek'] = array[1]
        opp, loc, homeGoals, awayGoals = self.parseOppLocScore(array[2])
        self.data['opponent'] = opp
        self.data['location'] = loc
        self.data['homeGoals'] = homeGoals
        self.data['awayGoals'] = awayGoals
        self.data['minsPlayed'] = array[3]
        self.data['goalsScored'] = array[4]
        self.data['assists'] = array[5]
        self.data['cleanSheets'] = array[6]
        self.data['goalsConceded'] = array[7]
        self.data['ownGoals'] = array[8]
        self.data['penaltiesSaved'] = array[9]
        self.data['penaltiesMissed'] = array[10]
        self.data['yellowCards'] = array[11]
        self.data['redCards'] = array[12]
        self.data['saves'] = array[13]
        self.data['bonus'] = array[14]
        self.data['EASportsPPI'] = array[15]
        self.data['netTransfers'] = array[16]
        self.data['value'] = array[17]
        self.data['points'] = array[18]

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

    def parseOppLocScore(self, string):
        opp = string[0:3]
        loc = string[4]
        goals = string.split(' ')[1].split('-')
        homeGoals = goals[0]
        awayGoals = goals[1]

        return opp, loc, homeGoals, awayGoals


def main():
    estimator = PlayerScoreEstimator(tableFilename=TABLE_FILENAME)
    player = Player(TEST_PLAYER_FILENAME)
    # score = estimator.estimateScore(player,'Queens Park Rangers','H')

    for teamName in teamNames:
        print teamName, estimator.estimateScore(player,teamName,'A')

if __name__ == '__main__':
    main()