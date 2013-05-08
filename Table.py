from bs4 import BeautifulSoup
from PLTeam import PLTeam

class Table(object):
    '''
    Description 
    '''
    def __init__(self, tableFilename=None, fixturesFolder = None, gameweek=None):
        self.gameweek = gameweek
        self.data = {}

        if tableFilename is not None:
            self.createTableFromTableFile(tableFilename)
        elif fixturesFolder is not None and gameweek is not None:
            self.createTableFromFixtureFolder(fixturesFolder, gameweek)
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

            plTeam = PLTeam(teamData)
            self[plTeam.teamName] = plTeam

    def createTableFromFixtureFolder(self, fixturesFolder, gameweek):
        #TODO - make sure everything works when gameweek = 0
        for i in range(1, gameweek+1):
            html = open(fixturesFolder + '/' + str(i))
            soup = BeautifulSoup(html)
            html.close()

            #parse file

            #update table

        #save table data

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
        # TODO - update 
        pass

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item