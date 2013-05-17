teamNames = {}
teamNames['Manchester United'] = 'Man Utd'
teamNames['Manchester City'] = 'Man City'
teamNames['Tottenham Hotspur'] = 'Tottenham'
teamNames['Chelsea'] = 'Chelsea'
teamNames['Everton'] = 'Everton'
teamNames['Arsenal'] = 'Arsenal'
teamNames['West Bromwich Albion'] = 'West Brom'
teamNames['Liverpool'] = 'Liverpool'
teamNames['Swansea City'] = 'Swansea'
teamNames['Stoke City'] = 'Stoke City'
teamNames['West Ham United'] = 'West Ham'
teamNames['Norwich City'] = 'Norwich'
teamNames['Fulham'] = 'Fulham'
teamNames['Sunderland'] = 'Sunderland'
teamNames['Newcastle United'] = 'Newcastle'
teamNames['Aston Villa'] = 'Aston Villa'
teamNames['Southampton'] = 'Southampton'
teamNames['Wigan Athletic'] = 'Wigan'
teamNames['Reading'] = 'Reading'
teamNames['Queens Park Rangers'] = 'QPR'

class PLTeam(object):
    def __init__(self, teamData=None, teamName=None):
        self.data = {}

        if teamData is not None:
            self.data['teamName'] = teamNames[teamData[0]]
            self.data['homePlayed'] = int(teamData[1])
            self.data['homeWon'] = int(teamData[2])
            self.data['homeDrawn'] = int(teamData[3])
            self.data['homeLost'] = int(teamData[4])
            self.data['homeGF'] = int(teamData[5])
            self.data['homeGA'] = int(teamData[6])
            self.data['homeGD'] = int(teamData[7])
            self.data['homePoints'] = int(teamData[8])

            self.data['awayPlayed'] = int(teamData[9])
            self.data['awayWon'] = int(teamData[10])
            self.data['awayDrawn'] = int(teamData[11])
            self.data['awayLost'] = int(teamData[12])
            self.data['awayGF'] = int(teamData[13])
            self.data['awayGA'] = int(teamData[14])
            self.data['awayGD'] = int(teamData[15])
            self.data['awayPoints'] = int(teamData[16])

            self.data['overallGD'] = int(teamData[17])
            self.data['overallPoints'] = int(teamData[18])
        else:
            self.data['teamName'] = teamNames[teamName]
            self.data['homePlayed'] = 0
            self.data['homeWon'] = 0
            self.data['homeDrawn'] = 0
            self.data['homeLost'] = 0
            self.data['homeGF'] = 0
            self.data['homeGA'] = 0
            self.data['homeGD'] = 0
            self.data['homePoints'] = 0

            self.data['awayPlayed'] = 0
            self.data['awayWon'] = 0
            self.data['awayDrawn'] = 0
            self.data['awayLost'] = 0
            self.data['awayGF'] = 0
            self.data['awayGA'] = 0
            self.data['awayGD'] = 0
            self.data['awayPoints'] = 0

            self.data['overallGD'] = 0
            self.data['overallPoints'] = 0

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

    def __repr__(self):
        return '%28s %12s %12s %12s\n'%(self['teamName'],self['homePlayed']+self['awayPlayed'],self['overallGD'],self['overallPoints'])


