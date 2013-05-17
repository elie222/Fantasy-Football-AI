'''
This class enables simulating a season of FPL.

Doesn't deal well with players that switched premier league teams in the middle of the year.
Doesn't deal with injuries.
'''

from bs4 import BeautifulSoup
import glob
from FPLAgent import FPLAgent
from PlayerScoreEstimator import PlayerScoreEstimator
from Table import Table
from Player import Player
from Fixtures import *

POINTS_COST_PER_TRANSFER = 4
MAX_FREE_TRANSFERS_SAVED = 2
STARTING_MONEY = 100

class Game:
    def __init__(self, fixturesFolder, playersFolder, agent, moneyAvailable=STARTING_MONEY):
        '''
        Expects all the player info to be in one folder with a different file for each player.
        '''
        self.fixturesFolder = fixturesFolder
        self.playersFolder = playersFolder
        
        # self.currentTable = Table(fixturesFolder=fixturesFolder, gameweek=0)
        self.allPlayersEnd = {} # this is all the player data in the playersFolder in dict format
        self.getAllPlayerDataEnd()

        self.agent = agent

        self.score = 0
        self.gameweek = 0
        self.freeTransfers = 0
        self.wildCards = 2 # change this
        self.moneyAvailable = moneyAvailable

        self.currentTeam = None
        self.previousTeam = None

    def getAllPlayerDataEnd(self):
        playerFilenames = glob.glob(self.playersFolder + '/*')

        for filename in playerFilenames:
            try:
                player = Player(filename=filename)
                allFixtures = []
                for fixture in player['fixture_history']['all']:
                    pf = PastFixture(fixture)
                    allFixtures.append(pf)
                player['fixture_history']['all'] = allFixtures
                self.allPlayersEnd[player['id']] = player
            except:
                pass

    def playGameweek(self,gameweekNo=None):
        if gameweekNo is not None:
            self.gameweek = gameweekNo
        else:
            self.gameweek += 1

        if self.freeTransfers < MAX_FREE_TRANSFERS_SAVED:
            self.freeTransfers += 1

        table = Table(fixturesFolder=self.fixturesFolder, gameweek=self.gameweek)
        players = self.getDataBeforeGameweek(gameweekNo)

        self.previousTeam = self.currentTeam
        self.currentTeam = self.agent.chooseTeam(players, table, self.previousTeam, self.moneyAvailable, self.freeTransfers, self.wildCards)

        self.moneyAvailable += (self.previousTeam.value - self.currentTeam.value)
        if self.moneyAvailable < 0:
            raise Exception('Money available has dropped below 0.')

        noOfTransfers = self.findNoOfTransfers()
        if noOfTransfers < self.freeTransfers:
            self.freeTransfers -= noOfTransfers
        else:
            self.freeTransfers = 0
            score -= (POINTS_COST_PER_TRANSFER*(noOfTransfers-self.freeTransfers))

        score += self.getGameweekScore(gameweekNo, self.currentTeam)

    def getDataBeforeGameweek(self, gameweekNo):
        '''
        Returns a dict mapping player ids to Player objects.
        Players that switched teams are a problem.
        TODO - make sure players that joined the pl in the middle of the year are not available
               to be chosen at the beginning of the year.
        TODO - futureFixtures for each player also have to be updated.
        '''
        gameweekData = {}

        for key in self.allPlayersEnd:
            player = self.allPlayersEnd[key]
            lastGameweekPlayed = 0
            currentValue = player['original_cost']
            pastFixtures = []
            for fixture in player['fixture_history']['all']:
                if fixture['gameweek'] <= gameweekNo:
                    pastFixtures.append(fixture)
                    if fixture['gameweek'] > lastGameweekPlayed:
                        lastGameweekPlayed = fixture['gameweek']
                        currentValue = fixture['value']

            player['fixture_history']['all'] = pastFixtures
            player['now_cost'] = currentValue

            # this data is incorrect for the player at this time, so setting it all to None
            # so that the agent doesn't mistakenly use this info.
            player['points_per_game'] = None
            player['total_points'] = None
            player['form'] = None
            player['status'] = None
            gameweekData[player['id']] = player

        return gameweekData

    def getGameweekScore(self, gameweekNo, team):
        '''
        gameweekNo - an integer between 1 and 38
        team - a Team object
        Returns the score for team in the given gameweek.
        Doesn't deal with transfer hits.
        '''
        score = 0

        nGks = 1
        nDefs = team.formation[0]
        nMids = team.formation[1]
        nAtts = team.formation[2]
        nCaptains = 1

        score += self.getScoreForPlayers(gameweekNo, team.gks, nGks)
        score += self.getScoreForPlayers(gameweekNo, team.defs, nDefs)
        score += self.getScoreForPlayers(gameweekNo, team.mids, nMids)
        score += self.getScoreForPlayers(gameweekNo, team.atts, nAtts)

        # captain/vice captain
        score += self.getScoreForPlayers(gameweekNo, [team.captain, team.viceCaptain], nCaptains)

        return score

    def getScoreForPlayers(self, gameweekNo, players, noToPlay):
        score = 0
        noAdded = 0

        for player in players:
            if noAdded == noToPlay:
                break
            playerScore, played = self.getPlayerScoreAndPlayed(playerId, gameweekNo)
            if played:
                score += playerScore
                noAdded += 1

        return score

    def getPlayerScoreAndPlayed(self, playerId, gameweekNo):
        '''
        Returns whether the player's score for the gameweek and whether he played or not.
        '''
        for fixture in self.allPlayersEnd[playerId]['fixture_history']['all']:
            if gameweekNo == fixture['gameweek']:
                if fixture['minsPlayed'] == 0:
                    0, False
                else:
                    return fixture['points'], True
        else:
            return 0, False

    def findNoOfTransfers(self):
        noOfTransfers = 0

        previousIdList = self.previousTeam.getPlayerIdsList()
        currentIdList = self.previousTeam.getPlayerIdsList()

        for prevId in previousIdList:
            if prevId not in currentIdList:
                noOfTransfers += 1

        return noOfTransfers

def main():
    agent = FPLAgent()
    game = Game(fixturesFolder='fixtures2012-13', playersFolder='26_3_2013', agent=agent, moneyAvailable=STARTING_MONEY)

    game.playGameweek(2)
    # print self.score
    # print self.currentTeam

if __name__ == '__main__':
    main()