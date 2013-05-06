import PlayerScoreEstimator

class FPLAgent:
	def __init__(self, playersFolder, tablePath, funds):
		self.playersFolder = playersFolder
		self.funds = funds
		self.team = None
		self.estimator = PlayerScoreEstimator(tablePath)

	def chooseTeam(self):
		return 0

def main():
	agent = FPLAgent('26_3_2013', '26_3_2013/tableHomeAndAway', 100)
	agent.chooseTeam()
	return 0

if __name__ == '__main__':
	main()