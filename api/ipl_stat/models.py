from django.db import models


class Match(models.Model):
    season = models.IntegerField()
    city = models.CharField(max_length=128, null=True, blank=True)
    date = models.DateField()
    team1 = models.CharField(max_length=128, null=True, blank=True)
    team2 = models.CharField(max_length=128, null=True, blank=True)
    toss_winner = models.CharField(max_length=128, null=True, blank=True)
    toss_decision = models.CharField(max_length=128, null=True, blank=True)
    result = models.CharField(max_length=128, null=True, blank=True)
    dl_applied = models.BooleanField(default=False)
    winner = models.CharField(max_length=128, null=True, blank=True)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    player_of_match = models.CharField(max_length=128, null=True, blank=True)
    venue = models.CharField(max_length=128, null=True, blank=True)
    umpire1 = models.CharField(max_length=128, null=True, blank=True)
    umpire2 = models.CharField(max_length=128, null=True, blank=True)
    umpire3 = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        unique_together = [
            "id",
            "season",
            "city",
            "date",
            "team1",
            "team2",
            "toss_winner",
            "toss_decision",
            "result",
            "dl_applied",
            "winner",
            "win_by_runs",
            "win_by_wickets",
            "player_of_match",
            "venue",
            "umpire1",
            "umpire2",
            "umpire3"
        ]

    def __str__(self):
        return str(id)


class Delivery(models.Model):
    match = models.ForeignKey(Match, on_delete=models.PROTECT)
    inning = models.IntegerField()
    batting_team = models.CharField(max_length=128, null=True, blank=True)
    bowling_team = models.CharField(max_length=128, null=True, blank=True)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=128, null=True, blank=True)
    non_striker = models.CharField(max_length=128, null=True, blank=True)
    bowler = models.CharField(max_length=128, null=True, blank=True)
    is_super_over = models.BooleanField(default=False)
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=128, null=True, blank=True)
    dismissal_kind = models.CharField(max_length=128, null=True, blank=True)
    fielder = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        unique_together = [
            "id",
            "match",
            "inning",
            "batting_team",
            "bowling_team",
            "over",
            "ball",
            "batsman",
            "non_striker",
            "bowler",
            "is_super_over",
            "wide_runs",
            "bye_runs",
            "legbye_runs",
            "noball_runs",
            "penalty_runs",
            "batsman_runs",
            "extra_runs",
            "total_runs",
            "player_dismissed",
            "dismissal_kind",
            "fielder"
        ]

    def __str__(self):
        return str(id)
