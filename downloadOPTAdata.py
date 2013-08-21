import cookielib
import mechanize
from bs4 import BeautifulSoup
import json
import time
from datetime import date
from datetime import datetime

# http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/

USERNAME = 'es222'
PASSWORD = 'jimmy89'

DOWNLOAD_PLAYER_DATA = False
DOWNLOAD_MATCH_DATA = True

def main():

	
	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	# Follows refresh 0 but not hangs on refresh > 0
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	# User-Agent (this is cheating, ok?)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	# The site we will navigate into, handling it's session
	br.open('http://members.fantasyfootballscout.co.uk/')

	br.select_form(nr=0)

	# User credentials
	br.form['username'] = USERNAME
	br.form['password'] = PASSWORD

	# Login
	br.submit()


	if DOWNLOAD_PLAYER_DATA:
		br.open('http://members.fantasyfootballscout.co.uk/player-stats/all-players/')

		player_links = [l for l in br.links(url_regex='player-profiles/')]

		for player_link in player_links[1:]:
			br.follow_link(player_link)
			html = br.response().read()

			player_name = player_link.attrs[2][1]
			filename = 'FFS_data/player_data/' + player_name + '.html'
			
			f = open(filename, 'w')
			f.write(html)
			f.close()

	if DOWNLOAD_MATCH_DATA:
		br.open('http://members.fantasyfootballscout.co.uk/matches/')

		match_links = [l for l in br.links(url_regex='matches/')]

		for match_link in match_links[1:]:
			br.follow_link(match_link)
			html = br.response().read()

			match_id = match_link.attrs[0][1].split('/')[2]
			filename = 'FFS_data/match_data_2012_13/' + match_id + '.html'
			
			f = open(filename, 'w')
			f.write(html)
			f.close()

if __name__ == '__main__':
	main()