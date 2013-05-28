'''
This class enables simulating a season of FPL.

Doesn't deal well with players that switched premier league teams in the middle of the year.
Doesn't deal with injuries.
'''
import sys
import glob
import cPickle as pickle
import os
import copy
from bs4 import BeautifulSoup

from FPLAgent import FPLAgent
from PlayerScoreEstimator import PlayerScoreEstimator
from Table import Table
from Player import Player
from Fixtures import *
import PLTeam

POINTS_COST_PER_TRANSFER = 4
MAX_FREE_TRANSFERS_SAVED = 2
STARTING_MONEY = 1000
NO_OF_GAMEWEEKS = 38

class Game:
    def __init__(self, fixturesFolder, playersFolder, agent, moneyAvailable=STARTING_MONEY):
        '''
        Expects all the player info to be in one folder with a different file for each player.
        '''
        self.fixturesFolder = fixturesFolder
        self.playersFolder = playersFolder

        # saving all the fixtures as FutureFixtures for all teams in the entire season
        # this may take a while. using pickling to speed things up.
        pickleFilename = 'allFutureFixtures_%s.pkl'%(fixturesFolder)
        if os.path.exists(pickleFilename):
            # print 'pickled file exists'
            pkl_file = open(pickleFilename, 'rb')
            self.allFixtures = pickle.load(pkl_file)
            pkl_file.close()
        else:
            # print 'no pickled file exists'
            self.allFixtures = {}
            for teamName in PLTeam.teamNames.values():
                self.allFixtures[teamName] = self.getAllFutureFixtures(teamName)

            output = open(pickleFilename, 'wb')
            pickle.dump(self.allFixtures, output)
            output.close()
        
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
            player = Player(filename=filename)
            allFixtures = []
            for fixture in player['fixture_history']['all']:
                pf = PastFixture(fixture)
                allFixtures.append(pf)
            player['fixture_history']['all'] = allFixtures
            self.allPlayersEnd[player['id']] = player

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
        self.currentTeam = self.agent.chooseTeam(players, table, self.previousTeam, self.moneyAvailable, self.freeTransfers, self.wildCards, gameweekNo)

        if self.previousTeam is None:
            #  no previous team
            self.moneyAvailable -= self.currentTeam.value
        else:
            self.moneyAvailable += (self.previousTeam.value - self.currentTeam.value)

        if self.moneyAvailable < 0:
            print self.moneyAvailable
            raise Exception('Money available has dropped below 0.')

        noOfTransfers = self.findNoOfTransfers()
        if noOfTransfers < self.freeTransfers:
            self.freeTransfers -= noOfTransfers
        else:
            self.freeTransfers = 0
            score -= (POINTS_COST_PER_TRANSFER*(noOfTransfers-self.freeTransfers))

        self.score += self.getGameweekScore(gameweekNo, self.currentTeam)

    def getDataBeforeGameweek(self, gameweekNo):
        '''
        Returns a dict mapping player ids to Player objects.
        Players that switched teams are a problem.
        TODO - make sure players that joined the pl in the middle of the year are not available
               to be chosen at the beginning of the year.
        '''
        gameweekData = {}

        for key in self.allPlayersEnd:
            player = copy.deepcopy(self.allPlayersEnd[key])
            lastGameweekPlayed = 0
            currentValue = player['original_cost']
            pastFixtures = []
            for fixture in player['fixture_history']['all']:
                if fixture['gameweek'] < gameweekNo:
                    pastFixtures.append(fixture)
                    if fixture['gameweek'] > lastGameweekPlayed:
                        lastGameweekPlayed = fixture['gameweek']
                        currentValue = fixture['value']

            futureFixtures = []
            for fixtureGW in self.allFixtures[player['team_name']]:
                if int(fixtureGW) >= gameweekNo:
                    futureFixtures.append(self.allFixtures[player['team_name']][fixtureGW])

            player['fixture_history']['all'] = pastFixtures
            player['fixtures']['all'] = futureFixtures
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
            playerScore, played = self.getPlayerScoreAndPlayed(player['id'], gameweekNo)
            if played:
                score += playerScore
                noAdded += 1

        # print score

        return score

    def getPlayerScoreAndPlayed(self, playerId, gameweekNo):
        '''
        Returns whether the player's score for the gameweek and whether he played or not.
        '''
        for fixture in self.allPlayersEnd[playerId]['fixture_history']['all']:
            if gameweekNo == fixture['gameweek']:
                if fixture['minsPlayed'] == 0:
                    return 0, False
                else:
                    return fixture['points'], True
        else:
            return 0, False

    def findNoOfTransfers(self):
        if self.previousTeam is None:
            return 0

        noOfTransfers = 0

        previousIdList = self.previousTeam.getPlayerIdsList()
        currentIdList = self.previousTeam.getPlayerIdsList()

        for prevId in previousIdList:
            if prevId not in currentIdList:
                noOfTransfers += 1

        return noOfTransfers

    def getAllFutureFixtures(self, teamName):
        '''
        Returns a dictionary mapping gameweeks to lists of fixtures for a team.
        This is all fixtures for the entire season for the team.
        A list could be empty, contain 1 fixture or 2 fixtures.
        The fixtures are FutureFixture objects.
        '''
        futureFixturesDict = {}

        for i in range(1,NO_OF_GAMEWEEKS+1):
            filename = '%s/%d'%(self.fixturesFolder, i)
            gwFixtures = parseFixturesFile(filename)

            futureFixtureList = []

            for gwFix in gwFixtures:
                if gwFix['homeTeam'] == teamName:
                    ff = FutureFixture()
                    ff['gameweek'] = i
                    ff['opponent'] = gwFix['awayTeam']
                    ff['location'] = 'H'
                    futureFixtureList.append(ff)
                elif gwFix['awayTeam'] == teamName:
                    ff = FutureFixture()
                    ff['gameweek'] = i
                    ff['opponent'] = gwFix['homeTeam']
                    ff['location'] = 'A'
                    futureFixtureList.append(ff)

            futureFixturesDict[str(i)] = futureFixtureList

        return futureFixturesDict

def main():
    agent = FPLAgent()
    game = Game(fixturesFolder='fixtures2012-13_final', playersFolder='20_5_2013', agent=agent, moneyAvailable=STARTING_MONEY)

    game.playGameweek(1)
    print game.score
    print game.currentTeam
    # game.playGameweek(11)
    # print game.score
    # print game.currentTeam

if __name__ == '__main__':
    main()