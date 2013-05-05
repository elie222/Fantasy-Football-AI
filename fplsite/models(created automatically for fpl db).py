# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

# see here: https://docs.djangoproject.com/en/dev/howto/legacy-databases/
# and here: https://docs.djangoproject.com/en/dev/howto/initial-data/

from __future__ import unicode_literals

from django.db import models

class Club(models.Model):
    idclub = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45L)
    class Meta:
        db_table = 'club'

class ClubNameMap(models.Model):
    idclub_name_map = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45L)
    club = models.ForeignKey(Club)
    class Meta:
        db_table = 'club_name_map'

class Competition(models.Model):
    idcompetition = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'competition'

class FantasyGameweek(models.Model):
    idfantasy_gameweek = models.IntegerField(primary_key=True)
    season = models.ForeignKey('FantasySeason')
    start_date = models.DateTimeField()
    free_transfers = models.IntegerField()
    class Meta:
        db_table = 'fantasy_gameweek'

class FantasyGameweekMatch(models.Model):
    idfantasy_gameweek_match = models.IntegerField(primary_key=True)
    gameweek = models.ForeignKey(FantasyGameweek)
    match = models.ForeignKey('MatchOverview')
    class Meta:
        db_table = 'fantasy_gameweek_match'

class FantasyManager(models.Model):
    idfantasy_manager = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45L)
    class Meta:
        db_table = 'fantasy_manager'

class FantasyPlayerCostChange(models.Model):
    idfantasy_player_cost_change = models.IntegerField(primary_key=True)
    gameweek = models.ForeignKey(FantasyGameweek)
    player = models.ForeignKey('Player')
    new_cost = models.IntegerField()
    vendor = models.ForeignKey('FantasyVendor')
    class Meta:
        db_table = 'fantasy_player_cost_change'

class FantasyPlayerMapping(models.Model):
    idfantasy_player_mapping = models.IntegerField(primary_key=True)
    season = models.ForeignKey('FantasySeason')
    vendor_player_id = models.IntegerField()
    player = models.ForeignKey('Player')
    class Meta:
        db_table = 'fantasy_player_mapping'

class FantasyPlayerPositionChange(models.Model):
    idfantasy_player_position_change = models.IntegerField(primary_key=True)
    gameweek = models.ForeignKey(FantasyGameweek)
    player = models.ForeignKey('Player')
    position = models.CharField(max_length=2L)
    vendor = models.ForeignKey('FantasyVendor')
    class Meta:
        db_table = 'fantasy_player_position_change'

class FantasySeason(models.Model):
    idfantasy_season = models.IntegerField(primary_key=True)
    vendor = models.ForeignKey('FantasyVendor')
    start_year = models.IntegerField()
    competition = models.ForeignKey(Competition)
    selection_rules = models.ForeignKey('FantasySelectionRules')
    gameweek_owner = models.ForeignKey(''self'')
    class Meta:
        db_table = 'fantasy_season'

class FantasySelectionRules(models.Model):
    idfantasy_selection_rules = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45L)
    squad_size = models.IntegerField()
    squad_gk_min = models.IntegerField()
    squad_gk_max = models.IntegerField()
    squad_df_min = models.IntegerField()
    squad_df_max = models.IntegerField()
    squad_mf_min = models.IntegerField()
    squad_mf_max = models.IntegerField()
    squad_fw_min = models.IntegerField()
    squad_fw_max = models.IntegerField()
    team_size = models.IntegerField()
    team_gk_min = models.IntegerField()
    team_gk_max = models.IntegerField()
    team_df_min = models.IntegerField()
    team_df_max = models.IntegerField()
    team_mf_min = models.IntegerField()
    team_mf_max = models.IntegerField()
    team_fw_min = models.IntegerField()
    team_fw_max = models.IntegerField()
    sub_gk_min = models.IntegerField()
    sub_gk_max = models.IntegerField()
    sub_df_min = models.IntegerField()
    sub_df_max = models.IntegerField()
    sub_mf_min = models.IntegerField()
    sub_mf_max = models.IntegerField()
    sub_fw_min = models.IntegerField()
    sub_fw_max = models.IntegerField()
    select_captain = models.IntegerField()
    select_vice_captain = models.IntegerField()
    budget = models.IntegerField()
    players_per_club_max = models.IntegerField()
    excess_transfer_penalty = models.IntegerField()
    sell_price_profit_proportion = models.FloatField()
    unused_free_transfers_bonus = models.IntegerField()
    uses_auto_subs = models.IntegerField()
    class Meta:
        db_table = 'fantasy_selection_rules'

class FantasySquad(models.Model):
    idfantasy_squad = models.IntegerField(primary_key=True)
    manager_name = models.CharField(max_length=45L)
    gameweek = models.ForeignKey(FantasyGameweek)
    points = models.IntegerField()
    budget = models.IntegerField()
    class Meta:
        db_table = 'fantasy_squad'

class FantasySquadSelection(models.Model):
    idfantasy_squad_selection = models.IntegerField(primary_key=True)
    squad = models.ForeignKey(FantasySquad)
    player = models.ForeignKey('Player')
    priority = models.FloatField()
    buy_cost = models.IntegerField()
    class Meta:
        db_table = 'fantasy_squad_selection'

class FantasyVendor(models.Model):
    idfantasy_vendor = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45L)
    url = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'fantasy_vendor'

class FantasyVendorUpdateHistory(models.Model):
    idfantasy_vendor_update_history = models.IntegerField(primary_key=True)
    vendor = models.ForeignKey(FantasyVendor)
    match = models.ForeignKey('MatchOverview')
    class Meta:
        db_table = 'fantasy_vendor_update_history'

class MatchAppearance(models.Model):
    idmatch_appearance = models.IntegerField(primary_key=True)
    side = models.ForeignKey('MatchSide')
    player = models.ForeignKey('Player')
    minute_on = models.IntegerField()
    minute_off = models.IntegerField()
    yellow_card = models.IntegerField()
    red_card = models.IntegerField()
    saves_made = models.IntegerField()
    penalties_missed = models.IntegerField()
    penalties_saved = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    team_scored = models.IntegerField()
    team_conceded = models.IntegerField()
    bonus_points = models.IntegerField()
    total_points = models.IntegerField()
    own_goals = models.IntegerField()
    class Meta:
        db_table = 'match_appearance'

class MatchGoal(models.Model):
    idmatch_goal = models.IntegerField(primary_key=True)
    side = models.ForeignKey('MatchSide')
    minute = models.IntegerField()
    scorer = models.ForeignKey(MatchAppearance, null=True, blank=True)
    is_own_goal = models.IntegerField(null=True, blank=True)
    assist_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'match_goal'

class MatchOverview(models.Model):
    idmatch = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    competition = models.ForeignKey(Competition)
    home_side = models.ForeignKey('MatchSide')
    away_side = models.ForeignKey('MatchSide')
    class Meta:
        db_table = 'match_overview'

class MatchSide(models.Model):
    idmatch_side = models.IntegerField(primary_key=True)
    club = models.ForeignKey(Club)
    goals = models.IntegerField()
    class Meta:
        db_table = 'match_side'

class Player(models.Model):
    idplayer = models.IntegerField(primary_key=True)
    family_name = models.CharField(max_length=45L, unique=True)
    given_name = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'player'

class PlayerAbsence(models.Model):
    idplayer_absence = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=45L, blank=True)
    description = models.CharField(max_length=45L, blank=True)
    start_probability = models.FloatField()
    class Meta:
        db_table = 'player_absence'

class PlayerNameMap(models.Model):
    idplayer_name_map = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45L)
    position = models.IntegerField(null=True, blank=True)
    club = models.ForeignKey(Club, null=True, blank=True)
    player = models.ForeignKey(Player)
    class Meta:
        db_table = 'player_name_map'

class PlayerPerformance(models.Model):
    idplayer_performance = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    team_scored = models.IntegerField()
    starts = models.IntegerField()
    subbed_on = models.IntegerField()
    unused = models.IntegerField()
    mins_played = models.IntegerField()
    max_mins_played = models.IntegerField()
    team_conceded = models.IntegerField()
    goals_penalties = models.IntegerField()
    goals_free_kicks = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    is_low_quality_league = models.IntegerField()
    class Meta:
        db_table = 'player_performance'

class PlayerTransfer(models.Model):
    idplayer_transfer = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club, null=True, blank=True)
    class Meta:
        db_table = 'player_transfer'

