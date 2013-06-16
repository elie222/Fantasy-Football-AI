# import sys
import random
from PlayerScoreEstimator import PlayerScoreEstimator
from Team import Team

GK_TYPE_NAME = 'Goalkeeper'
DEF_TYPE_NAME = 'Defender'
MID_TYPE_NAME = 'Midfielder'
ATT_TYPE_NAME = 'Forward'

class ValueAgent(object):
	'''
	This agent just picks the best value team. Not very smart, but is a basic team whose cost is always very low.
	'''
	def __init__(self, prevYearTableFilename):
		'''
		prevYearTable - filename of the previous year's final table. Helps to pick a team in the first few gameweeks.
		'''
		self.prevYearTable = Table(prevYearTableFilename)

	def chooseTeam(self, allPlayers, currentTable, previousTeam, moneyAvailable, freeTransfers, wildCards, gameweek):
		'''
		allPlayers - a dict mapping player ids to Player objects to pick a team from.
		currentTable - a Table object representing the current table
		previousTeam - a Team object representing the team to be updated
		moneyAvailable - amount of money available to spend
		freeTransfers - no. of free transfers available
		wildCards - no. of wildcards available
		gameweek - current gameweek
		'''
		estimator = PlayerScoreEstimator(currentTable)

		playersInfoList = [] # a list of dicts

		for key in allPlayers:
			try:
				player = allPlayers[key]
				score = estimator.estimateScoreMultipleGames(player,player['fixtures']['all'],gameweek,discount=0.7)
				value = score/player['now_cost']
				likelihoodOfPlaying = 1

				playerInfo = {}
				playerInfo['player'] = player
				playerInfo['score'] = score
				playerInfo['value'] = value
				playerInfo['likelihoodOfPlaying'] = likelihoodOfPlaying

				playersInfoList.append(playerInfo)
			except:
				raise

		playersInfoList = sorted(playersInfoList, key=lambda piDict: piDict['value'], reverse=True)
		gksPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == GK_TYPE_NAME]
		defsPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == DEF_TYPE_NAME]
		midsPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == MID_TYPE_NAME]
		attsPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == ATT_TYPE_NAME]

		if previousTeam is None or True: # 'or True' is for DEBUGGING PURPOSES ONLY
			# pick completely new team
			gkCount = 0
			defCount = 0
			midount = 0
			attCount = 0
			
			teamList = []
			teamList = self.addPlayers(teamList, gksPIList, 2)
			teamList = self.addPlayers(teamList, defsPIList, 5)
			teamList = self.addPlayers(teamList, midsPIList, 5)
			teamList = self.addPlayers(teamList, attsPIList, 3)

			team = Team(teamList, formation=[3,4,3], captain=None, viceCaptain=None)
			
			return team
		else:
			print 'HERE'
			# improve old team
			# TODO
			pass

	def addPlayers(self, teamList, playersInfoList, noOfPlayers):
		'''
		This function assumes that playersInfoList is sorted in the correct order.
		It will add the top noOfPlayers from the given playersInfoList to the current team and return the new team.
		'''
		count = 0

		for playerInfo in playersInfoList:
			teamList.append(playerInfo['player'])
			count += 1
			if count == noOfPlayers:
				break

		return teamList

class RandomAgent(object):
	'''
	This agent picks a certain no. of random teams and chooses the one it thinks it will score highest.
	An improved random agent will only look at the best value and highest scoring players and ignore the rubbish ones.
	TODO - this isn't considering changing captain each week or thinking about the bench and switching players each week.
	Should change it so it is.
	'''
	def __init__(self, prevYearTableFilename, noOfIterations, discount=1, weeksToLookAhead=6):
		self.noOfIterations = noOfIterations
		self.discount = discount
		self.weeksToLookAhead = weeksToLookAhead
		self.prevYearTable = Table(prevYearTableFilename)

	def chooseTeam(self, allPlayers, currentTable, previousTeam, moneyAvailable, freeTransfers, wildCards, gameweek):
		estimator = None
		if gameweek < 5:
			estimator = PlayerScoreEstimator(self.prevYearTable)
		else:	
			estimator = PlayerScoreEstimator(currentTable)

		playersInfoList = [] # a list of dicts

		for key in allPlayers:
			try:
				player = allPlayers[key]
				score = estimator.estimateScoreMultipleGames(player,player['fixtures']['all'],gameweek,discount=self.discount)
				value = score/player['now_cost']
				likelihoodOfPlaying = 1

				playerInfo = {}
				playerInfo['player'] = player
				playerInfo['score'] = score
				playerInfo['now_cost'] = player['now_cost']
				playerInfo['value'] = value
				playerInfo['likelihoodOfPlaying'] = likelihoodOfPlaying

				playersInfoList.append(playerInfo)
			except:
				raise

		gksPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == GK_TYPE_NAME]
		defsPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == DEF_TYPE_NAME]
		midsPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == MID_TYPE_NAME]
		attsPIList = [pi for pi in playersInfoList if pi['player']['type_name'] == ATT_TYPE_NAME]

		if previousTeam is None or True: # 'or True' is for DEBUGGING PURPOSES ONLY
			# pick completely new team

			highestEstScore = 0
			highestEstScoreTeam = None

			for i in range(self.noOfIterations):
				gkCount = 0
				defCount = 0
				midount = 0
				attCount = 0
				
				teamList = []
				teamList = self.addRandomPlayers(teamList, gksPIList, 2, GK_TYPE_NAME)
				teamList = self.addRandomPlayers(teamList, defsPIList, 5, DEF_TYPE_NAME)
				teamList = self.addRandomPlayers(teamList, midsPIList, 5, MID_TYPE_NAME)
				teamList = self.addRandomPlayers(teamList, attsPIList, 3, ATT_TYPE_NAME)

				# estimate team score
				estScore = 0

				# check that team does not have 3 players from the same club. would be more efficient to check this while adding players.
				# TODO

				teamCost = 0
				for player, score in teamList:
					estScore += score

					# check that team cost is <= money available. would be more efficient to check this while adding players.
					teamCost += player['now_cost']
					if teamCost > moneyAvailable:
						continue

				if estScore > highestEstScore:
					highestEstScore = estScore
					highestEstScoreTeam = []
					for player, score in teamList:
						highestEstScoreTeam.append(player)

			team = Team(highestEstScoreTeam, formation=[3,4,3], captain=None, viceCaptain=None)
			
			return team
		else:
			print 'HERE'
			# improve old team
			# TODO
			pass

	def addRandomPlayers(self, teamList, playersInfoList, noOfPlayers, position):
		'''
		teamList - a list of player, score tuples (different to addPlayer() in FPLAgent).
		'''
		count = 0

		while True:
			chosenIndex = random.randint(0,len(playersInfoList)-1)
			chosen = playersInfoList[chosenIndex]
			if (chosen['player'], chosen['score']) in teamList:
				continue
			else:
				teamList.append((chosen['player'], chosen['score']))

			count += 1
			if count == noOfPlayers:
				break

		return teamList

	def estimateTeamScore(self, teamList, gameweek, estimator):
		estScoreTotal = 0

		for i in range(self.weeksToLookAhead):
			estScoreGameweek = 0
			for player in teamList:
				# gwFixtures = [fixtures in ]
				estimator.estScore(player, player['fixtures']['all'][gameweek+i])#TODO working on this function atm

		# estimate score for each player for each gw
		# choose starting 11, subs, captain and vice-captain

		# workout score. give sum points to subs. eg. 0.3, 0.2, 0.1. maybe a bit more

		return estScoreTotal

def main():
	pass

if __name__ == '__main__':
	main()