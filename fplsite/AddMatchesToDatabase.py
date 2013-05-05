# setup sys.path first if needed
import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/django')

# tell django which settings module to use
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'fplsite.settings'

from pl_table.models import Team, Match, PLTableRow
from bs4 import BeautifulSoup
import datetime

def add_match(year, gameweek, date, home_team, away_team, home_goals, away_goals):
    home_team = Team.objects.get(short_name=home_team)
    away_team = Team.objects.get(short_name=away_team)
    match = Match(year=year, gameweek = gameweek, date=date, home_team=home_team, away_team=away_team, home_goals=home_goals, away_goals=away_goals)
    match.save()

    from CreateTableInfo import updatePLTableInfo
    updatePLTableInfo(year,gameweek,match)
    # updatePLForTeamThatPlayed(year,gameweek,home_team,match)
    # updatePLForTeamThatPlayed(year,gameweek,away_team,match)

def find_gameweek(fixture_table):
    a = fixture_table.find('caption', class_='ismStrongCaption')
    gameweek = a.get_text().split(' ')[1]

    return int(gameweek)

def find_matches(fixture_table):
    matches = []

    table_rows = fixture_table.find_all('tr', class_='ismFixture ismResult')
    
    for tr in table_rows:
        match = {}
        tds = tr.find_all('td')

        date_str = tds[0].get_text()#date is in this format: '22 Aug 19:45'
        date = datetime.datetime.strptime(date_str, "%d %b %H:%M")
        if date.month < 8:
            date = date.replace(year = 2013)
        else:
            date = date.replace(year = 2012)
        match['date'] = date

        match['home_team'] = tds[1].get_text()
        match['away_team'] = tds[5].get_text()

        score = tds[3].get_text().split(' - ')
        match['home_goals'] = int(score[0])
        match['away_goals'] = int(score[1])

        matches.append(match)

    return matches

def addMatchesFromDir(directory, start_gameweek, end_gameweek):
    for i in range(start_gameweek, end_gameweek+1):
        f = open(directory + '/' + str(i) + '.html')
        soup = BeautifulSoup(f)
        f.close()

        fixture_table = soup.find(id='ismFixtureTable')

        year = 2012
        gameweek = find_gameweek(fixture_table)#should always be equal to i
        assert(gameweek==i)
        matches = find_matches(fixture_table)

        for match in matches:
            add_match(year, gameweek, match['date'], match['home_team'], match['away_team'], match['home_goals'], match['away_goals'])

        teams_that_didnt_play = find_teams_that_didnt_play(matches)

        for team_id in teams_that_didnt_play:
            from CreateTableInfo import updateTeamThatDidntPlay
            updateTeamThatDidntPlay(year,gameweek,team_id)


def find_teams_that_didnt_play(matches):
    all_teams = Team.objects.all()
    all_ids = [team.id for team in all_teams]
    teams_that_played_home = [match['home_team'] for match in matches]
    teams_that_played_away = [match['away_team'] for match in matches]
    teams_that_played = teams_that_played_home + teams_that_played_away
    ids_that_didnt_play = [team.id for team in all_teams if not team.short_name in teams_that_played]

    return ids_that_didnt_play

def main():
    directory = 'GW History 2013'
    start_gameweek = 1
    end_gameweek = 30

    addMatchesFromDir(directory, start_gameweek, end_gameweek)

    # qs = PLTableRow.objects.filter(gameweek=28, team_id=1).order_by('-id')
    # print qs

if __name__ == '__main__':
    main()