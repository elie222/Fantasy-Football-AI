import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/django')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'fplsite.settings'

from pl_table.models import PLTableRow, Match, Team

POINTS_FOR_WIN = 3
POINTS_FOR_DRAW = 1
POINTS_FOR_LOSS = 0

def updatePLTableInfo(year, gameweek, match):

    # home team

    #assuming no such thing as a triple gameweek
    replace_home = False

    prev_week_home_team = None
    
    qs_home = PLTableRow.objects.filter(year=year, gameweek=gameweek, team_id=match.home_team)
    #already played this week
    if len(qs_home) == 1:
        prev_week_home_team = qs_home[0]
        replace_home = True
    else:
        #assuming that a team will play in at least one of the first 2 gws of the season
        #haven't yet played a game in the league
        if gameweek == 1:
            prev_week_home_team = PLTableRow(year=year,gameweek=gameweek,team_id=match.home_team,home_games_played=0,
            home_won=0,home_drawn=0,home_lost=0,home_points=0,home_gf=0,home_ga=0,
            away_games_played=0,away_won=0,away_drawn=0,away_lost=0,
            away_gf=0,away_ga=0,away_points=0)
        #have already played a game
        else:
            qs_home = PLTableRow.objects.filter(year=year, gameweek=gameweek-1, team_id=match.home_team)
            #played last week
            if len(qs_home) == 1:
                prev_week_home_team = qs_home[0]
            #will only get here if a team hasn't played 2 gws in a row. bug if they haven't played 3 in a row
            else:
                prev_week_home_team = PLTableRow.objects.filter(year=year, gameweek=gameweek-2, team_id=match.home_team)[0]


    # qs_home = PLTableRow.objects.filter(year=year, gameweek=gameweek, team_id=match.home_team).order_by('-id')
    # replace_home = qs_home[0]
    # #if haven't yet played this week
    # if not len(qs_home) == 1:
    #     qs_home = PLTableRow.objects.filter(year=year, gameweek=gameweek-1, team_id=match.home_team).order_by('-id')

    # qs_away = PLTableRow.objects.filter(year=year, gameweek=gameweek, team_id=match.away_team).order_by('-id')
    # replace_away=qs_away[0]
    # #if haven't yet played this week
    # if not len(qs_home) == 1:
    #     qs_home = PLTableRow.objects.filter(year=year, gameweek=gameweek-1, team_id=match.away_team).order_by('-id')

    # if len(qs_home) == 0:
    #     prev_week_home_team = PLTableRow(year=year,gameweek=gameweek,team_id=match.home_team,home_games_played=0,
    #     home_won=0,home_drawn=0,home_lost=0,home_points=0,home_gf=0,home_ga=0,
    #     away_games_played=0,away_won=0,away_drawn=0,away_lost=0,
    #     away_gf=0,away_ga=0,away_points=0)

    # if len(qs_away) ==0 :
    #     prev_week_away_team = PLTableRow(year=year,gameweek=gameweek,team_id=match.away_team,home_games_played=0,
    #     home_won=0,home_drawn=0,home_lost=0,home_points=0,home_gf=0,home_ga=0,
    #     away_games_played=0,away_won=0,away_drawn=0,away_lost=0,
    #     away_gf=0,away_ga=0,away_points=0)

    year = year
    gameweek = gameweek
    team_id = match.home_team
    home_games_played = prev_week_home_team.home_games_played + 1
    if match.home_goals > match.away_goals:
        home_won = prev_week_home_team.home_won + 1
        home_drawn = prev_week_home_team.home_drawn
        home_lost = prev_week_home_team.home_lost
        home_points = prev_week_home_team.home_points + POINTS_FOR_WIN
    elif match.home_goals == match.away_goals:
        home_won = prev_week_home_team.home_won
        home_drawn = prev_week_home_team.home_drawn + 1
        home_lost = prev_week_home_team.home_lost
        home_points = prev_week_home_team.home_points + POINTS_FOR_DRAW
    else:
        home_won = prev_week_home_team.home_won
        home_drawn = prev_week_home_team.home_drawn
        home_lost = prev_week_home_team.home_lost + 1
        home_points = prev_week_home_team.home_points + POINTS_FOR_LOSS
    home_gf = prev_week_home_team.home_gf + match.home_goals
    home_ga = prev_week_home_team.home_ga + match.away_goals

    away_games_played = prev_week_home_team.away_games_played
    away_won = prev_week_home_team.away_won
    away_drawn = prev_week_home_team.away_drawn
    away_lost = prev_week_home_team.away_lost
    away_gf = prev_week_home_team.away_gf
    away_ga = prev_week_home_team.away_ga
    away_points = prev_week_home_team.away_points

    tr_home = PLTableRow(year=year,gameweek=gameweek,team_id=team_id,home_games_played=home_games_played,
        home_won=home_won,home_drawn=home_drawn,home_lost=home_lost,home_points=home_points,home_gf=home_gf,home_ga=home_ga,
        away_games_played=away_games_played,away_won=away_won,away_drawn=away_drawn,away_lost=away_lost,
        away_gf=away_gf,away_ga=away_ga,away_points=away_points)

    if replace_home:
        replace_id = prev_week_home_team.id
        prev_week_home_team = tr_home
        prev_week_home_team.id = replace_id
        prev_week_home_team.save()
    else:
        tr_home.save()

    # if replace_home is None:
    #     tr_home.save()
    # else:
    #     replace_home.year=year
    #     replace_home.gameweek=gameweek
    #     replace_home.team_id=team_id
    #     replace_home.home_games_played=home_games_played
    #     replace_home.home_won=home_won
    #     replace_home.home_drawn=home_drawn
    #     replace_home.home_lost=home_lost
    #     replace_home.home_points=home_points
    #     replace_home.home_gf=home_gf
    #     replace_home.home_ga=home_ga
    #     replace_home.away_games_played=away_games_played
    #     replace_home.away_won=away_won
    #     replace_home.away_drawn=away_drawn
    #     replace_home.away_lost=away_lost
    #     replace_home.away_gf=away_gf
    #     replace_home.away_ga=away_ga
    #     replace_home.away_points=away_points

    #     replace_home.save()





    # away team

    #assuming no such thing as a triple gameweek
    replace_away = False

    prev_week_away_team = None
    
    qs_away = PLTableRow.objects.filter(year=year, gameweek=gameweek, team_id=match.away_team)
    #already played this week
    if len(qs_away) == 1:
        prev_week_away_team = qs_away[0]
        replace_away = True
    else:
        #assuming that a team will play in at least one of the first 2 gws of the season
        #haven't yet played a game in the league
        if gameweek == 1:
            prev_week_away_team = PLTableRow(year=year,gameweek=gameweek,team_id=match.home_team,home_games_played=0,
            home_won=0,home_drawn=0,home_lost=0,home_points=0,home_gf=0,home_ga=0,
            away_games_played=0,away_won=0,away_drawn=0,away_lost=0,
            away_gf=0,away_ga=0,away_points=0)
        #have already played a game
        else:
            qs_away = PLTableRow.objects.filter(year=year, gameweek=gameweek-1, team_id=match.away_team)
            #played last week
            if len(qs_away) == 1:
                prev_week_away_team = qs_away[0]
            #will only get here if a team hasn't played 2 gws in a row. bug if they haven't played 3 in a row
            else:
                prev_week_away_team = PLTableRow.objects.filter(year=year, gameweek=gameweek-2, team_id=match.away_team)[0]


    year = year
    gameweek = gameweek
    team_id = match.away_team
    away_games_played = prev_week_away_team.away_games_played + 1
    if match.away_goals > match.home_goals:
        away_won = prev_week_away_team.away_won + 1
        away_drawn = prev_week_away_team.away_drawn
        away_lost = prev_week_away_team.away_lost
        away_points = prev_week_away_team.away_points + POINTS_FOR_WIN
    elif match.away_goals == match.home_goals:
        away_won = prev_week_away_team.away_won
        away_drawn = prev_week_away_team.away_drawn + 1
        away_lost = prev_week_away_team.away_lost
        away_points = prev_week_away_team.away_points + POINTS_FOR_DRAW
    else:
        away_won = prev_week_away_team.away_won
        away_drawn = prev_week_away_team.away_drawn
        away_lost = prev_week_away_team.away_lost + 1
        away_points = prev_week_away_team.away_points + POINTS_FOR_LOSS
    away_gf = prev_week_away_team.away_gf + match.away_goals
    away_ga = prev_week_away_team.away_ga + match.home_goals

    home_games_played = prev_week_away_team.home_games_played
    home_won = prev_week_away_team.home_won
    home_drawn = prev_week_away_team.home_drawn
    home_lost = prev_week_away_team.home_lost
    home_gf = prev_week_away_team.home_gf
    home_ga = prev_week_away_team.home_ga
    home_points = prev_week_away_team.home_points

    tr_away = PLTableRow(year=year,gameweek=gameweek,team_id=team_id,away_games_played=away_games_played,
        away_won=away_won,away_drawn=away_drawn,away_lost=away_lost,away_points=away_points,away_gf=away_gf,away_ga=away_ga,
        home_games_played=home_games_played,home_won=home_won,home_drawn=home_drawn,home_lost=home_lost,
        home_gf=home_gf,home_ga=home_ga,home_points=home_points)

    if replace_away:
        replace_id = prev_week_away_team.id
        prev_week_away_team = tr_away
        prev_week_away_team.id = replace_id
        prev_week_away_team.save()
    else:
        tr_away.save()
    
    # if replace_away is None:
    #     tr_away.save()
    # else:
    #     replace_away = tr_away
    #     replace_away.save()

    # if replace_away is None:
    #     tr_away.save()
    # else:
    #     replace_away.year=year
    #     replace_away.gameweek=gameweek
    #     replace_away.team_id=team_id
    #     replace_away.home_games_played=home_games_played
    #     replace_away.home_won=home_won
    #     replace_away.home_drawn=home_drawn
    #     replace_away.home_lost=home_lost
    #     replace_away.home_points=home_points
    #     replace_away.home_gf=home_gf
    #     replace_away.home_ga=home_ga
    #     replace_away.away_games_played=away_games_played
    #     replace_away.away_won=away_won
    #     replace_away.away_drawn=away_drawn
    #     replace_away.away_lost=away_lost
    #     replace_away.away_gf=away_gf
    #     replace_away.away_ga=away_ga
    #     replace_away.away_points=away_points

    #     if gameweek == 1 and team_id.id==19:
    #         print 'READING GW1 away (4)'

    #     replace_away.save()

def updateTeamThatDidntPlay(year, gameweek, team_id):

    tr = None

    team = Team.objects.get(id=team_id)

    prev_week_tr = None
    
    qs = PLTableRow.objects.filter(year=year, gameweek=gameweek-1, team_id=team).order_by('-id')

    if len(qs) > 0:
        prev_tr = qs[0]

        tr = PLTableRow(year=year,gameweek=gameweek,team_id=team,home_games_played=prev_tr.home_games_played,
        home_won=prev_tr.home_won,home_drawn=prev_tr.home_drawn,home_lost=prev_tr.home_lost,home_points=prev_tr.home_points,home_gf=prev_tr.home_gf,home_ga=prev_tr.home_ga,
        away_games_played=prev_tr.away_games_played,away_won=prev_tr.away_won,away_drawn=prev_tr.away_drawn,away_lost=prev_tr.away_lost,
        away_gf=prev_tr.away_gf,away_ga=prev_tr.away_ga,away_points=prev_tr.away_points)
    else:
        tr = PLTableRow(year=year,gameweek=gameweek,team_id=team,home_games_played=0,
        home_won=0,home_drawn=0,home_lost=0,home_points=0,home_gf=0,home_ga=0,
        away_games_played=0,away_won=0,away_drawn=0,away_lost=0,
        away_gf=0,away_ga=0,away_points=0)

    tr.save()