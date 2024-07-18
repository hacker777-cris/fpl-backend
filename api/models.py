from django.db import models


class Fixture(models.Model):
    date = models.DateField()
    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)
    stadium = models.CharField(max_length=255)
    time = models.TimeField()
    competition_name = models.CharField(max_length=255)
    week = models.IntegerField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.date}"


class PlayerStats(models.Model):
    player_name = models.CharField(max_length=255)
    fpl_price = models.DecimalField(max_digits=5, decimal_places=2)
    starts = models.IntegerField()
    time_played = models.IntegerField()
    appearances = models.IntegerField()
    sub_on = models.IntegerField()
    sub_off = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    fantasy_assists = models.IntegerField()
    total_assists = models.IntegerField()
    goals_conceded = models.IntegerField()
    own_goals_conceded = models.IntegerField()
    clean_sheets = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    fpl_points = models.IntegerField()
    minutes_per_fpl_point = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.player_name


class Player(models.Model):
    chance_of_playing_next_round = models.IntegerField(null=True, blank=True)
    chance_of_playing_this_round = models.IntegerField(null=True, blank=True)
    code = models.IntegerField()
    cost_change_event = models.IntegerField()
    cost_change_event_fall = models.IntegerField()
    cost_change_start = models.IntegerField()
    cost_change_start_fall = models.IntegerField()
    dreamteam_count = models.IntegerField()
    element_type = models.IntegerField()
    ep_next = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ep_this = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    event_points = models.IntegerField()
    first_name = models.CharField(max_length=100)
    form = models.DecimalField(max_digits=5, decimal_places=1)
    id = models.IntegerField(primary_key=True)
    in_dreamteam = models.BooleanField()
    news = models.TextField()
    news_added = models.DateTimeField(null=True, blank=True)
    now_cost = models.IntegerField()
    photo = models.CharField(max_length=100)
    points_per_game = models.DecimalField(max_digits=5, decimal_places=1)
    second_name = models.CharField(max_length=100)
    selected_by_percent = models.DecimalField(max_digits=5, decimal_places=1)
    special = models.BooleanField()
    squad_number = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=1)
    team = models.IntegerField()
    team_code = models.IntegerField()
    total_points = models.IntegerField()
    transfers_in = models.IntegerField()
    transfers_in_event = models.IntegerField()
    transfers_out = models.IntegerField()
    transfers_out_event = models.IntegerField()
    value_form = models.DecimalField(max_digits=5, decimal_places=1)
    value_season = models.DecimalField(max_digits=5, decimal_places=1)
    web_name = models.CharField(max_length=100)
    minutes = models.IntegerField()
    goals_scored = models.IntegerField()
    assists = models.IntegerField()
    clean_sheets = models.IntegerField()
    goals_conceded = models.IntegerField()
    own_goals = models.IntegerField()
    penalties_saved = models.IntegerField()
    penalties_missed = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    saves = models.IntegerField()
    bonus = models.IntegerField()
    bps = models.IntegerField()
    influence = models.DecimalField(max_digits=6, decimal_places=1)
    creativity = models.DecimalField(max_digits=6, decimal_places=1)
    threat = models.DecimalField(max_digits=6, decimal_places=1)
    ict_index = models.DecimalField(max_digits=6, decimal_places=1)
    starts = models.IntegerField()
    expected_goals = models.DecimalField(max_digits=5, decimal_places=2)
    expected_assists = models.DecimalField(max_digits=5, decimal_places=2)
    expected_goal_involvements = models.DecimalField(max_digits=5, decimal_places=2)
    expected_goals_conceded = models.DecimalField(max_digits=5, decimal_places=2)
    influence_rank = models.IntegerField()
    influence_rank_type = models.IntegerField()
    creativity_rank = models.IntegerField()
    creativity_rank_type = models.IntegerField()
    threat_rank = models.IntegerField()
    threat_rank_type = models.IntegerField()
    ict_index_rank = models.IntegerField()
    ict_index_rank_type = models.IntegerField()
    corners_and_indirect_freekicks_order = models.IntegerField(null=True, blank=True)
    corners_and_indirect_freekicks_text = models.TextField(null=True, blank=True)
    direct_freekicks_order = models.IntegerField(null=True, blank=True)
    direct_freekicks_text = models.TextField(null=True, blank=True)
    penalties_order = models.IntegerField(null=True, blank=True)
    penalties_text = models.TextField(null=True, blank=True)
    expected_goals_per_90 = models.DecimalField(max_digits=4, decimal_places=2)
    saves_per_90 = models.DecimalField(max_digits=4, decimal_places=2)
    expected_assists_per_90 = models.DecimalField(max_digits=4, decimal_places=2)
    expected_goal_involvements_per_90 = models.DecimalField(
        max_digits=4, decimal_places=2
    )
    expected_goals_conceded_per_90 = models.DecimalField(max_digits=4, decimal_places=2)
    goals_conceded_per_90 = models.DecimalField(max_digits=4, decimal_places=2)
    now_cost_rank = models.IntegerField()
    now_cost_rank_type = models.IntegerField()
    form_rank = models.IntegerField()
    form_rank_type = models.IntegerField()
    points_per_game_rank = models.IntegerField()
    points_per_game_rank_type = models.IntegerField()
    selected_rank = models.IntegerField()
    selected_rank_type = models.IntegerField()
    starts_per_90 = models.DecimalField(max_digits=4, decimal_places=2)
    clean_sheets_per_90 = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = "players"  # Optional: Specify the database table name if needed

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


class Team(models.Model):
    code = models.IntegerField()
    draw = models.IntegerField()
    form = models.CharField(max_length=255, null=True, blank=True)
    id = models.IntegerField(primary_key=True)
    loss = models.IntegerField()
    name = models.CharField(max_length=255)
    played = models.IntegerField()
    points = models.IntegerField()
    position = models.IntegerField()
    short_name = models.CharField(max_length=3)
    strength = models.IntegerField()
    team_division = models.CharField(max_length=255, null=True, blank=True)
    unavailable = models.BooleanField()
    win = models.IntegerField()
    strength_overall_home = models.IntegerField()
    strength_overall_away = models.IntegerField()
    strength_attack_home = models.IntegerField()
    strength_attack_away = models.IntegerField()
    strength_defence_home = models.IntegerField()
    strength_defence_away = models.IntegerField()
    pulse_id = models.IntegerField()

    def __str__(self):
        return self.name


class FantasyFixtureStats(models.Model):
    code = models.IntegerField()
    event = models.IntegerField()
    finished = models.BooleanField()
    finished_provisional = models.BooleanField()
    id = models.IntegerField(primary_key=True)
    kickoff_time = models.DateTimeField()
    minutes = models.IntegerField()
    provisional_start_time = models.BooleanField()
    started = models.BooleanField()
    team_a = models.IntegerField()
    team_a_score = models.IntegerField(null=True, blank=True)
    team_h = models.IntegerField()
    team_h_score = models.IntegerField(null=True, blank=True)
    team_h_difficulty = models.IntegerField()
    team_a_difficulty = models.IntegerField()
    pulse_id = models.IntegerField()

    def __str__(self):
        return f"{self.team_h} vs {self.team_a}"


class PlayerPosition(models.Model):
    id = models.IntegerField(primary_key=True)
    plural_name = models.CharField(max_length=255)
    plural_name_short = models.CharField(max_length=3)
    singular_name = models.CharField(max_length=255)
    singular_name_short = models.CharField(max_length=3)
    squad_select = models.IntegerField()
    squad_min_select = models.IntegerField(null=True, blank=True)
    squad_max_select = models.IntegerField(null=True, blank=True)
    squad_min_play = models.IntegerField()
    squad_max_play = models.IntegerField()
    ui_shirt_specific = models.BooleanField()
    sub_positions_locked = models.JSONField()
    element_count = models.IntegerField()

    def __str__(self):
        return self.singular_name


class GameweekStats(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    deadline_time = models.DateTimeField()
    release_time = models.DateTimeField(null=True, blank=True)
    average_entry_score = models.IntegerField()
    finished = models.BooleanField()
    data_checked = models.BooleanField()
    highest_scoring_entry = models.IntegerField(null=True, blank=True)
    deadline_time_epoch = models.IntegerField()
    deadline_time_game_offset = models.IntegerField()
    highest_score = models.IntegerField(null=True, blank=True)
    is_previous = models.BooleanField()
    is_current = models.BooleanField()
    is_next = models.BooleanField()
    cup_leagues_created = models.BooleanField()
    h2h_ko_matches_created = models.BooleanField()
    ranked_count = models.IntegerField()
    transfers_made = models.IntegerField()
    most_selected = models.IntegerField(null=True, blank=True)
    most_transferred_in = models.IntegerField(null=True, blank=True)
    top_element = models.IntegerField(null=True, blank=True)
    top_element_info = models.JSONField(null=True, blank=True)
    most_captained = models.IntegerField(null=True, blank=True)
    most_vice_captained = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
