# import sys
from PlayerScoreEstimator import PlayerScoreEstimator
from Team import Team

GK_TYPE_NAME = 'Goalkeeper'
DEF_TYPE_NAME = 'Defender'
MID_TYPE_NAME = 'Midfielder'
ATT_TYPE_NAME = 'Forward'

class FPLAgent(object):
    def chooseTeam(self, allPlayers, currentTable, previousTeam, moneyAvailable, freeTransfers, wildCards):
        '''
        allPlayers - a dict mapping player ids to Player objects to pick a team from.
        currentTable - a Table object representing the current table
        previousTeam - a Team object representing the team to be updated
        moneyAvailable - amount of money available to spend
        freeTransfers - no. of free transfers available
        wildCards - no. of wildcards available
        '''
        estimator = PlayerScoreEstimator(currentTable)

        playersInfoList = [] # a list of dicts

        for key in allPlayers:
            try:
                player = allPlayers[key]
                score = estimator.estimateScoreMultipleGames(player,player['fixtures']['all'])
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

        if previousTeam is None:
            # pick completely new team
            gkCount = 0
            defCount = 0
            midount = 0
            attCount = 0
            
            teamList = []
            teamList = self.addPlayers(teamList, playersInfoList, 2, GK_TYPE_NAME)
            teamList = self.addPlayers(teamList, playersInfoList, 5, DEF_TYPE_NAME)
            teamList = self.addPlayers(teamList, playersInfoList, 5, MID_TYPE_NAME)
            teamList = self.addPlayers(teamList, playersInfoList, 3, ATT_TYPE_NAME)

            team = Team(teamList, formation=[3,4,3], captain=None, viceCaptain=None)
            # self.team.captain = playerScoreDict[0]['player']
            # self.team.viceCaptain = playerScoreDict[1]['player']
            
            return team
        else:
            # improve old team
            # TODO
            pass

    def addPlayers(self, teamList, playersInfoList, noOfPlayers, position):
        '''
        This function assumes that playersInfoList is sorted in the correct order.
        It will add the top noOfPlayers from the given position to the current team and return the new team.
        '''
        count = 0

        for playerInfo in playersInfoList:
            if playerInfo['player']['type_name'] == position:
                teamList.append(playerInfo['player'])
                count += 1
                if count == noOfPlayers:
                    break

        return teamList

def main():
    pass

if __name__ == '__main__':
    main()