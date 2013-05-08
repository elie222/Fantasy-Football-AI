from bs4 import BeautifulSoup
from PLTeam import PLTeam

class Table(object):
    '''
    Can be viewed as a dict mapping team names to 
    '''
    def __init__(self, filename, gameweek=None):
        self.gameweek = gameweek
        self.data = {}
        self.createTable(filename)

    def createTable(self, filename):
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

            self[team.teamName] = PLTeam(teamData)

        self.initAverages()

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

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        self.data[key] = item