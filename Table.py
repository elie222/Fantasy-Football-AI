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
            self.fixturesFolder = fixturesFolder
            self.createTableFromFixtureFolder(gameweek)
        else:
            raise Exception('Invalid arguments to Table constructor.')

        self.initAverages()

    # TODO - check that the next functions produce the same Table files
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

            plTeam = PLTeam.PLTeam(teamData=teamData)
            self[plTeam['teamName']] = plTeam

    def createTableFromFixtureFolder(self, gameweek):
        '''
        This creates the table as it was at the start of the gameweek before any games had been played.
        '''
        for teamName in PLTeam.teamNames:
            self[PLTeam.teamNames[teamName]] = PLTeam.PLTeam(teamName=teamName)

        for i in range(1, gameweek):
            f = open(self.fixturesFolder + '/' + str(i))
            soup = BeautifulSoup(f.read())
            f.close()

            #parse file
            fixtures = soup.find_all("tr", class_="ismFixture")

            for fixture in fixtures:
                homeTeam = fixture.find("td", class_="ismHomeTeam").get_text()
                awayTeam = fixture.find("td", class_="ismAwayTeam").get_text()

                score = fixture.find("td", class_="ismScore").get_text()
                splitScore = score.split(' - ')
                homeScore = int(splitScore[0])
                awayScore = int(splitScore[1])
                
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
            self[teamName]['homePlayed'] += 1
            if gf > ga:
                self[teamName]['homeWon'] += 1
                self[teamName]['homePoints'] += 3
            elif gf == ga:
                self[teamName]['homeDrawn'] += 1
                self[teamName]['homePoints'] += 1
            else:
                self[teamName]['homeLost'] += 1
            
            self[teamName]['homeGF'] += gf
            self[teamName]['homeGA'] += ga
            self[teamName]['homeGD'] += (gf - ga)
        else:
            self[teamName]['awayPlayed'] += 1
            if gf > ga:
                self[teamName]['awayWon'] += 1
                self[teamName]['awayPoints'] += 3
            elif gf == ga:
                self[teamName]['awayDrawn'] += 1
                self[teamName]['awayPoints'] += 1
            else:
                self[teamName]['awayLost'] += 1

            self[teamName]['awayGF'] += gf
            self[teamName]['awayGA'] += ga
            self[teamName]['awayGD'] += (gf - ga)

        self[teamName]['overallGD'] += (gf - ga)
        self[teamName]['overallPoints'] = self[teamName]['homePoints'] + self[teamName]['awayPoints']

    def initAverages(self):
        self.avgHomeGF = self.calcAverage('homeGF')
        self.avgHomeGA = self.calcAverage('homeGA')
        self.avgAwayGF = self.calcAverage('awayGF')
        self.avgAwayGA = self.calcAverage('awayGA')

    def calcAverage(self, avgType):
        goals = 0
        for team in self.data:
            goals += self[team][avgType]
        return float(goals)/len(self.data)

    def addTeam(self, team):
        self[team.teamName] = team

    def updateTableTillGW(self, gameweek):
        # TODO
        pass

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item

    def __repr__(self):
        result = 'Table, Gameweek %d\n'%(self.gameweek)
        result += '%28s %12s %12s %12s\n'%('Team','GP','GD','Points')
        for key in self.data:
            result += str(self[key])

        return result

