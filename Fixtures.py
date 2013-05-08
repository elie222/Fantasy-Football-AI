class PastFixture(object):
    def __init__(self, array):
        self.data = {}

        self.data['date'] = array[0]
        self.data['gameweek'] = array[1]
        opp, loc, homeGoals, awayGoals = self.parseOppLocScore(array[2])
        self.data['opponent'] = opp
        self.data['location'] = loc
        self.data['homeGoals'] = homeGoals
        self.data['awayGoals'] = awayGoals
        self.data['minsPlayed'] = array[3]
        self.data['goalsScored'] = array[4]
        self.data['assists'] = array[5]
        self.data['cleanSheets'] = array[6]
        self.data['goalsConceded'] = array[7]
        self.data['ownGoals'] = array[8]
        self.data['penaltiesSaved'] = array[9]
        self.data['penaltiesMissed'] = array[10]
        self.data['yellowCards'] = array[11]
        self.data['redCards'] = array[12]
        self.data['saves'] = array[13]
        self.data['bonus'] = array[14]
        self.data['EASportsPPI'] = array[15]
        self.data['netTransfers'] = array[16]
        self.data['value'] = array[17]
        self.data['points'] = array[18]

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

    def parseOppLocScore(self, string):
        opp = string[0:3]
        loc = string[4]
        goals = string.split(' ')[1].split('-')
        homeGoals = goals[0]
        awayGoals = goals[1]

        return opp, loc, homeGoals, awayGoals

class FutureFixture(object):
    def __init__(self, array):
        self.data = {}

        self.data['date'] = array[0]
        self.data['gameweek'] = self.parseGameweek(array[1])
        opp, loc = self.parseOppLoc(array[2])
        self.data['opponent'] = opp
        self.data['location'] = loc

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

    def parseOppLoc(self, string):
        '''
        Example:
        Input: 'West Brom (H)'
        Output: ['West Brom', 'H']
        '''
        if string == '-':
            return None, None

        splitString = string.split(' (')
        opp = splitString[0]
        loc = splitString[1][0]

        return opp, loc

    def parseGameweek(self, string):
        '''
        Example:
        Input: 'Gameweek 31'
        Output: 31
        '''
        return int(string.split(' ')[1])