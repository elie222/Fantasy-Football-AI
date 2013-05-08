import PlayerScoreEstimator

GK_TYPE_NAME = 'Goalkeeper'
DEF_TYPE_NAME = 'Defender'
MID_TYPE_NAME = 'Midfielder'
ATT_TYPE_NAME = 'Forward'

class FPLAgent(object):
	def chooseTeam(self, allPlayers, currentTable, previousTeam, moneyAvailable, freeTransfers, wildCards):

		self.estimator = PlayerScoreEstimator(currentTable)

			playerScoreDict = {} # a dict of dicts

		    for playerFilename in playerFilenames:
		        try:
		            player = Player(playerFilename)
		            score = estimator.estimateScoreMultipleGames(player,player['fixtures']['all'])
		            value = score/player['now_cost']
		            likelihoodOfPlaying = 1

		            playerInfo = {}
		            playerInfo['player'] = player
		            playerInfo['score'] = score
		            playerInfo['value'] = value
		            playerInfo['likelihoodOfPlaying'] = likelihoodOfPlaying

		            playerScoreDict[player['web_name']] = playerInfo
		        except:
		            pass

		    playerScoreDict = sorted(playerScoreDict,key=itemgetter('value'), reverse=True) # not sure this will work

		if previousTeam is None:
			# pick completely new team
			gkCount = 0
			defCount = 0
			midount = 0
			attCount = 0
			
			teamList = []
			teamList = addPlayers(teamList, playerScoreDict, 2, GK_TYPE_NAME)
			teamList = addPlayers(teamList, playerScoreDict, 5, DEF_TYPE_NAME)
			teamList = addPlayers(teamList, playerScoreDict, 5, MID_TYPE_NAME)
			teamList = addPlayers(teamList, playerScoreDict, 3, ATT_TYPE_NAME)

			team = Team(teamList, formation=[3,4,3], captain=None, viceCaptain=None)
			# self.team.captain = playerScoreDict[0]['player']
			# self.team.viceCaptain = playerScoreDict[1]['player']
			
			return team
		else:
			# improve old team
			# TODO
			pass

	def addPlayers(self, teamList, psDict, noOfPlayers, position):
		count = 0
		for ps in psDict:
			if ps['player']['type_name'] == position:
				teamList.append(ps)
				count += 1
				if count = noOfPlayers:
					break
		return teamList

def main():
	pass

if __name__ == '__main__':
	main()