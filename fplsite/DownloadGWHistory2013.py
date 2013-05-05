import os
import urllib

NO_OF_GAMEWEEKS = 38

directory = 'GW History 2013'

if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(NO_OF_GAMEWEEKS):
	html = urllib.urlopen('http://fantasy.premierleague.com/fixtures/'+ str(i+1) +'/').read()
	f = open(directory + '/' + str(i+1) + '.html', 'w')
	f.write(html)
	f.close()