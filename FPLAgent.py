import PlayerScoreEstimator

class FPLAgent(object):
	# def __init__(self, playersFolder, tablePath):
	# 	self.playersFolder = playersFolder
	# 	self.team = None
	# 	self.estimator = PlayerScoreEstimator(tablePath)

	def chooseTeam(self, allPlayers, currentTable, previousTeam, freeTransfers, moneyAvailable):

		if previousTeam is None:
			# pick completely new team
			self.team = Team([], formation=[3,4,3], captain=None, viceCaptain=None)
		else:
			# improve old team

def main():
	pass

if __name__ == '__main__':
	main()