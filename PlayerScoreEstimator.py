from bs4 import BeautifulSoup
import json
import glob

from Table import Table
from PLTeam import PLTeam
from Player import Player
from Fixtures import PastFixture, FutureFixture

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


class PlayerScoreEstimator:
    def __init__(self, table):
        self.table = table

    def estimateScore(self,player,fixture):
        '''
        Will just return 0 for all players in the first week since the table will be all zeros.
        TODO: if a team has not yet scored or conceded, the oppStrength will be 0. Problem. Causes division by 0.
        '''
        print player, fixture

        if fixture['opponent'] is None:
            print 'returning 0. no opp'
            return 0

        if self.table.avgAwayGF == 0 or self.table.avgAwayGA == 0 or self.table.avgHomeGF == 0 or self.table.avgHomeGA == 0:
            print 'returning 0. new table'
            return 0

        opponentName = fixture['opponent']
        location = fixture['location']

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
            print 'location must be H or A.'
            raise

        print 'here'

        return self.calcMiscPPG(player)+(locAdv*((self.calcDefPPG(player)/oppAttStrength)+(self.calcAttPPG(player)*oppDefStrength)))

    def estimateScoreMultipleGames(self,player,fixtureList,discount=1):
        '''
        TODO: implement discount (apply to gameweeks, not to fixtures)
        '''
        estScore = 0

        print fixtureList

        futureFixture = None
        for fixture in fixtureList:
            print fixture
            futureFixture = FutureFixture(fixture)
            estScore += self.estimateScore(player, futureFixture)
            print 'EST_SCORE: %d'%estScore

        print estScore
        import sys
        sys.exit()

        return estScore

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
        for fixture in player['fixture_history']['all']:
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
        for fixture in player['fixture_history']['all']:
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

        print player['fixture_history']['all']

        for fixture in player['fixture_history']['all']:
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




def main():

    folder = '26_3_2013'
    tableFilename = 'tableHomeAndAway.html'
    playerFilenames = glob.glob(folder + '/*')
    playerFilenames.remove(folder + '/' + tableFilename)

    table = Table(folder+'/'+tableFilename)
    estimator = PlayerScoreEstimator(table)

    playerScoreDict = {}

    player = Player(playerFilenames[0])
    score = estimator.estimateScoreMultipleGames(player,player['fixtures']['all'])
    playerScoreDict[player['web_name']] = score

    # for playerFilename in playerFilenames:
    #     try:
    #         player = Player(playerFilename)
    #         score = estimator.estimateScoreMultipleGames(player,player['fixtures']['all'])
    #         playerScoreDict[player['web_name']] = score
    #     except:
    #         pass
    #         # print 'ERROR FOR:', playerFilename

    import operator
    sortedPlayerScoreList = sorted(playerScoreDict.iteritems(), key=operator.itemgetter(1))

    for tup in sortedPlayerScoreList:
        print tup[0], tup[1]

if __name__ == '__main__':
    main()