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

TOTAL_NO_OF_GAMES = 38


class PlayerScoreEstimator:
    def __init__(self, table):
        self.table = table

    def estimateScore(self,player,fixture):
        '''
        Will just return 0 for all players in the first week since the table will be all zeros.
        TODO: if a team has not yet scored or conceded, the oppStrength will be 0. Problem. Causes division by 0.
        '''
        if fixture['opponent'] is None:
            # print 'returning 0. no opp'
            return 0

        # for the first 4 weeks we're only basing our estimate off of last season's stats
        if len(player['fixture_history']['all']) < 4:
            return self.estimateScoreFirstGW(player, fixture)

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

        miscPoints = self.calcMiscPPG(player)
        defPoints = 0
        if oppAttStrength == 0:
            # to avoid division by zero
            defPoints = locAdv*self.calcDefPPG(player)/0.7
        else:
            defPoints = locAdv*self.calcDefPPG(player)/oppAttStrength
        if oppDefStrength == 0:
            # to avoid multiplying by zero
            attPoints = self.calcAttPPG(player)*0.7
        else:
            attPoints = self.calcAttPPG(player)*oppDefStrength

        return miscPoints + defPoints + attPoints

    def estimateScoreFirstGW(self, player, fixture):
        if len(player['season_history']) == 0:
            # new to the PL. not going to risk picking this player basically.
            return 0

        lastSeason = player['season_history'][-1]
        minsPlayed = lastSeason[1]
        points = lastSeason[-1]
        gamesPlayed = minsPlayed/90 # not exact, but whatever

        # not taking a risk in picking players that didn't play a lot last year.
        # possibly increase this no. - but then players like Cisse or Jelavic that joined in Jan might be knocked out the list, which we might not want to do.
        if gamesPlayed < 10:
            return 0

        return float(points)/gamesPlayed

    def estimateScoreMultipleGames(self,player,fixtureList,currentGW,discount=1):
        estScore = 0

        for GWFixtureList in fixtureList:
            for fixture in GWFixtureList:
                estScore += (discount**(fixture['gameweek']-currentGW))*self.estimateScore(player, fixture)

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

        # print player['fixture_history']['all']

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