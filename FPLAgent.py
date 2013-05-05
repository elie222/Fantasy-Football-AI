class FPLAgent:
	def __init__(self, funds):
		self.funds = funds
		self.team = self.chooseTeam(funds)

	def chooseTeam(self, funds):
		return 0