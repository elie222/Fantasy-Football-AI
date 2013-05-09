from bs4 import BeautifulSoup
import PLTeam

class Table(object):
    '''
    Description 
    '''
    def __init__(self, tableFilename=None, fixturesFolder=None, gameweek=1):
        self.gameweek = gameweek
        self.data = {}

        if tableFilename is not None:
            self.createTableFromTableFile(tableFilename)
        elif fixturesFolder is not None and gameweek is not None:
            self.createTableFromFixtureFolder(gameweek)
        else:
            raise Exception('Invalid arguments to Table constructor.')

        self.initAverages()

    def createTableFromTableFile(self, filename):
        html = open(filename, 'r')
        soup = BeautifulSoup(html)
        html.close()

        teams = soup.find_all("td", class_="club-names")
        for team in teams:
            teamData = []
            teamData.append(team.get_text())
            nextRow = team.find_next_sibling()
            while (nextRow is not None):
                teamData.append(nextRow.get_text())
                nextRow = nextRow.find_next_sibling()

            plTeam = PLTeam.PLTeam(teamData)
            self[plTeam.teamName] = plTeam

    def createTableFromFixtureFolder(self, gameweek):
        '''
        This creates the table as it was at the start of the gameweek before any games had been played.
        '''
        for teamName in PLTeam.teamNames:
            self[teamName] = PLTeam.PLTeam(teamName=teamName)

        for i in range(1, gameweek):
            html = open(self.fixturesFolder + '/' + str(i))
            soup = BeautifulSoup(html)
            html.close()

            #parse file
            fixtures = soup.find_all("td", class_="ismFixture")
            for fixture in fixtures:
                homeTeam = fixtures.find("td", class_="ismHomeTeam")
                awayTeam = fixtures.find("td", class_="ismAwayTeam")

                score = fixtures.find("td", class_="ismScore")
                splitScore = score.split(' - ')
                homeScore = splitScore[0]
                awayScore = splitScore[1]
                
                #update table
                self.updateTeam(homeTeam, homeScore, awayScore, True)
                self.updateTeam(awayTeam, awayScore, homeScore, False)

    def updateTeam(self, teamName, gf, ga, atHome):
        '''
        teamName - the name of the team to update
        gf - no. of goals scored by the team in the match
        ga - no. of goals let in by the team in the match
        atHome - True if the team played at home. False if it played away
        '''
        if atHome:
            self['homePlayed'] += 1
            if gf > ga:
                self['homeWon'] += 1
                self['homePoints'] += 3
            elif gf == ga:
                self['homeDrawn'] += 1
                self['homePoints'] += 1
            else:
                self['homeLost'] += 1
            self['homeGF'] += gf
            self['homeGA'] += ga
            self['homeGD'] += (gf - ga)
        else:
            self['awayPlayed'] += 1
            if gf > ga:
                self['awayWon'] += 1
                self['awayPoints'] += 3
            elif gf == ga:
                self['awayDrawn'] += 1
                self['awayPoints'] += 1
            else:
                self['awayLost'] += 1
            self['awayGF'] += gf
            self['awayGA'] += ga
            self['awayGD'] += (gf - ga)

        self['overallGD'] += (gf - ga)
        self['overallPoints'] = self['homePoints'] + self['awayPoints']

    def initAverages(self):
        self.avgHomeGF = self.calcAverage('homeGF')
        self.avgHomeGA = self.calcAverage('homeGA')
        self.avgAwayGF = self.calcAverage('awayGF')
        self.avgAwayGA = self.calcAverage('awayGA')

    def calcAverage(self, avgType):
        goals = 0
        for team in self.data:
            goals += self[team][avgType]
        return goals/len(self.data)

    def addTeam(self, team):
        self[team.teamName] = team

    def updateTableTillGW(self, gameweek):
        # TODO
        pass

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item