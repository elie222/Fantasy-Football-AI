from bs4 import BeautifulSoup
import FPLAgent
import PlayerScoreEstimator

class Game:
	def __init__(self, fixturesFolder, playersFolder, agent):
		self.fixturesFolder = fixturesFolder
		self.playersFolder = playersFolder
		self.agent = self.agent

		self.score = 0
		self.gameweek = 0
		self.freeTransfers = 1

	def playGameweek(self,gameweekNo, agent):
		team = agent.chooseTeam()

	def getGameweekData(self, gameweekNo):
		'''
		Returns a dict mapping player ids to the players score for that week.
		'''
		gameweekData = {}

		playerFilenames = glob.glob(self.playersFolder + '/*')

		for playerFile in playerFilenames:
			try:
	            player = Player(playerFilename)
	            gameweekData[p['id']] = player
			except:
				pass

		return gameweekData

	def getGameweekScore(self, gameweekNo, team):
		'''
		gameweekNo - an integer between 1 and 38
		team - a Team object
		Returns the score for team in the given gameweek.
		'''
		score = 0

		gameweekData = getGameweekData(gameweekNo)

		for player in team:
			score += gameweekData[player['id']]

		return score

class Gameweek:
	def __init__(self, playersFolder):
		self.playersFolder = playersFolder











def main():
	agent = FPLAgent('26_3_2013', '26_3_2013/tableHomeAndAway', 100)
	game = Game('fixtures2012-13', agent)
	return 0

if __name__ == '__main__':
	main()