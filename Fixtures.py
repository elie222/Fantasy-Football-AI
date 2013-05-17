class PastFixture(object):
    def __init__(self, array):
        self.data = {}

        # print array

        self['date'] = array[0]
        self['gameweek'] = array[1]
        opp, loc, homeGoals, awayGoals = self.parseOppLocScore(array[2])
        self['opponent'] = opp
        self['location'] = loc
        self['homeGoals'] = homeGoals
        self['awayGoals'] = awayGoals
        self['minsPlayed'] = array[3]
        self['goalsScored'] = array[4]
        self['assists'] = array[5]
        self['cleanSheets'] = array[6]
        self['goalsConceded'] = array[7]
        self['ownGoals'] = array[8]
        self['penaltiesSaved'] = array[9]
        self['penaltiesMissed'] = array[10]
        self['yellowCards'] = array[11]
        self['redCards'] = array[12]
        self['saves'] = array[13]
        self['bonus'] = array[14]
        self['EASportsPPI'] = array[15]
        self['netTransfers'] = array[16]
        self['value'] = array[17]
        self['points'] = array[18]

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

    def __repr__(self):
        return 'PastFixture. Gameweek: %s. Opp: %s. Loc: %s'%(self['gameweek'], self['opponent'], self['location'])

class FutureFixture(object):
    def __init__(self, array):
        self.data = {}

        self['date'] = array[0]
        self['gameweek'] = self.parseGameweek(array[1])
        opp, loc = self.parseOppLoc(array[2])
        self['opponent'] = opp
        self['location'] = loc

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

    def __repr__(self):
        return 'FutureFixture. Gameweek: %s. Opp: %s. Loc: %s'%(self['gameweek'], self['opponent'], self['location'])