import urllib
from bs4 import BeautifulSoup
import json

ROOT_FOLDER = '26_3_2013'

def findPlayerIDs(soup):

	playerIDs = []

	playerDivs = soup.find_all("div", class_="ismPitchElement")

	for div in playerDivs:
		firstLine = str(div).split('\n')[0]
		jsonStr = firstLine[firstLine.index('{'):firstLine.index('}')+1]
		obj = json.loads(jsonStr)
		playerIDs.append(obj['id'])

	return playerIDs

def calculateTeamScore(playerIDs):
	score = 0

	for playerID in playerIDs:
		jsonPlayer = open(ROOT_FOLDER + '/' + str(playerID), 'r')
		htmlPlayer = jsonPlayer.read()
		try:
			player = json.loads(htmlPlayer)
		except:
			print 'there was an error for file: ' + playerFile
			print "Error: ", sys.exc_info()[0]
			jsonPlayer.close()
			continue
		jsonPlayer.close()

		#print player['web_name']

		from calculatePlayerStats import calculatePlayerExpScore
		score += calculatePlayerExpScore(player, int(sys.argv[2]), float(sys.argv[3]))

		playerInfo = []
		playerInfo.append(player['web_name'])
		playerInfo.append(player['team_name'])
		playerInfo.append(float(player['now_cost'])/10)
		playerInfo.append(player['total_points'])
		playerInfo.append(player['status'])
		playerInfo.append(expectedPoints)
		playerInfo.append(expectedPoints/(float(player['now_cost'])/10))
		team1Score += expectedPoints
	print team1Score

	return score

def main():
	html = open('Team139903.html' ,'r')
	soup = BeautifulSoup(html)
	html.close()

	playerIDs = findPlayerIDs(soup)

	score = calculateTeamScore(playerIDs)
	print score

if  __name__ =='__main__':
    main()