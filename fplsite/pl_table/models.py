from django.db import models

class PLTableRow(models.Model):
    year = models.PositiveIntegerField()
    gameweek = models.PositiveIntegerField()
    team_id = models.ForeignKey('Team')#should really be team not team_id. too much hassle to change it now

    home_games_played = models.PositiveIntegerField()
    home_won = models.PositiveIntegerField()
    home_drawn = models.PositiveIntegerField()
    home_lost = models.PositiveIntegerField()
    home_gf = models.PositiveIntegerField()
    home_ga = models.PositiveIntegerField()
    # home_gd = models.IntegerField()
    home_points = models.IntegerField()#can be calculated using the other data

    away_games_played = models.PositiveIntegerField()
    away_won = models.PositiveIntegerField()
    away_drawn = models.PositiveIntegerField()
    away_lost = models.PositiveIntegerField()
    away_gf = models.PositiveIntegerField()
    away_ga = models.PositiveIntegerField()
    # away_gd = models.IntegerField()
    away_points = models.IntegerField()#can be calculated using the other data

    # overall_games_played = models.PositiveIntegerField()
    # overall_won = models.PositiveIntegerField()
    # overall_drawn = models.PositiveIntegerField()
    # overall_lost = models.PositiveIntegerField()
    # overall_gf = models.PositiveIntegerField()
    # overall_ga = models.PositiveIntegerField()
    # overall_gd = models.IntegerField()
    # overall_points = models.IntegerField()
    
    def get_overall_games_played(self):
        return self.home_games_played + self.away_games_played

    def get_overall_games_won(self):
        return self.home_won + self.away_won
    def get_overall_games_drawn(self):
        return self.home_drawn + self.away_drawn
    def get_overall_games_won(self):
        return self.home_lost + self.away_lost

    def get_home_gd(self):
        return self.get_home_gf - self.get_home_ga
    def get_away_gd(self):
        return self.get_away_gf() - self.get_away_ga()

    def get_overall_gf(self):
        return self.gf + self.gf
    def get_overall_ga(self):
        return self.home_ga + self.away_ga
    def get_overall_gd(self):
        return self.get_overall_gf() - self.get_overall_ga()

    def get_overall_points(self):
        return self.home_points + self.away_points

    def __unicode__(self):
        return 'YEAR: ' + str(self.year) + '. GAMEWEEK: ' + str(self.gameweek) + '. TEAM: ' + str(self.team_id)

class Team(models.Model):
    name = models.CharField(max_length=20, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    short_name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return 'TEAM_NAME: ' + self.short_name + '. TEAM_ID: ' + str(self.id)

class Match(models.Model):
    year = models.PositiveIntegerField()
    gameweek = models.PositiveIntegerField()
    date = models.DateTimeField()
    home_team = models.ForeignKey('Team', related_name='team_playing_at_home')
    away_team = models.ForeignKey('Team', related_name='team_playing_away')
    home_goals = models.PositiveIntegerField()
    away_goals = models.PositiveIntegerField()

# class Player(models.Model):
#     web_name = models.CharField(max_length=20)
#     first_name = models.CharField(max_length=15)
#     second_name = models.CharField(max_length=15)
#     team_name = models.ForeignKey('Team', )
