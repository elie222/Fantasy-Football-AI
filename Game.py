'''
This class enables simulating a season of FPL.
'''

from bs4 import BeautifulSoup
import FPLAgent
import PlayerScoreEstimator

POINTS_COST_PER_TRANSFER = 4
MAX_FREE_TRANSFERS_SAVED = 2
STARTING_MONEY = 100

class Game:
	def __init__(self, fixturesFolder, playersFolder, agent, moneyAvailable=STARTING_MONEY):
		self.fixturesFolder = fixturesFolder
		self.playersFolder = playersFolder
		self.agent = agent

		self.score = 0
		self.gameweek = 0
		self.freeTransfers = 0
		self.wildCards = 2
		self.moneyAvailable = moneyAvailable

		self.currentTeam = None
		self.previousTeam = None

	def playGameweek(self,gameweekNo):
		self.gameweek += 1
		if self.freeTransfers < MAX_FREE_TRANSFERS_SAVED:
			self.freeTransfers += 1

		self.previousTeam = self.currentTeam
		self.currentTeam = self.agent.chooseTeam(self.previousTeam, self.freeTransfers, self.moneyAvailable, self.wildCards)

		noOfTransfers = self.findNoOfTransfers()
		if noOfTransfers < self.freeTransfers:
			self.freeTransfers -= noOfTransfers
		else:
			self.freeTransfers = 0
			score -= (POINTS_COST_PER_TRANSFER*(noOfTransfers-self.freeTransfers))

		score += self.getGameweekScore(gameweekNo, self.currentTeam)

		# TODO - update self.moneyAvailable

	def getGameweekData(self, gameweekNo):
		'''
		Returns a dict mapping player ids to PastFixture objects.
		'''
		gameweekData = {}

		playerFilenames = glob.glob(self.playersFolder + '/*')

		for playerFile in playerFilenames:
			try:
	            player = Player(playerFilename)
	            for fixture in player['fixture_history']['all']:
	            	pastFixture = PastFixture(fixture)
	            	gameweekData[player['id']] = pastFixture
			except:
				pass

		return gameweekData

	def getGameweekScore(self, gameweekNo, team):
		'''
		gameweekNo - an integer between 1 and 38
		team - a Team object
		Returns the score for team in the given gameweek.
		Doesn't deal with transfer hits.
		'''
		score = 0

		gameweekData = getGameweekData(gameweekNo)

		nGks = 1
		nDefs = team.formation[0]
		nMids = team.formation[1]
		nAtts = team.formation[2]
		nCaptains = 1

		score += self.getScoreForPlayers(team.gks, nGks)
		score += self.getScoreForPlayers(team.defs, nDefs)
		score += self.getScoreForPlayers(team.mids, nMids)
		score += self.getScoreForPlayers(team.atts, nAtts)

		# captain/vice captain
		score += self.getScoreForPlayers([team.captain, team.viceCaptain], nCaptains)

		return score

	def getScoreForPlayers(self, players, noToPlay):
		score = 0
		noAdded = 0

		for player in players:
			if noAdded == noToPlay:
				break
			if not gameweekData[player['id']]['minsPlayed'] == 0:
				score += gameweekData[player['id']]['points']
				noAdded += 1

		return score

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
	game = Game('fixtures2012-13', '26_3_2013', agent, moneyAvailable=STARTING_MONEY)

if __name__ == '__main__':
	main()