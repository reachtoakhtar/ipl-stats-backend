import logging
import math

from django.db.models import Count, Q, Sum
from rest_framework import serializers

from ipl_stat.models import Delivery

__author__ = "akhtar"

logger = logging.getLogger(__name__)


class WinSerializer(serializers.Serializer):
    x = serializers.CharField(max_length=128, source="winner")
    y = serializers.IntegerField(source="no_of_wins")


class TossWinSerializer(serializers.Serializer):
    x = serializers.CharField(max_length=128, source="toss_winner")
    y = serializers.IntegerField(source="no_of_wins")


class TossWinDecisionSerializer(serializers.Serializer):
    x = serializers.CharField(max_length=128, source="toss_winner")
    no_of_wins = serializers.IntegerField()
    field_times = serializers.IntegerField()
    bat_times = serializers.IntegerField()
    y = serializers.SerializerMethodField()

    def get_y(self, value):
        percentage = value["bat_times"] * 100 / value["no_of_wins"]
        return math.ceil(percentage)


class RunWinSerializer(serializers.Serializer):
    winner = serializers.CharField(max_length=128)
    max_win_margin = serializers.IntegerField()


class WicketWinSerializer(serializers.Serializer):
    winner = serializers.CharField(max_length=128)
    max_win_wickets = serializers.IntegerField()


class PlayerOfMatchSerializer(serializers.Serializer):
    player_of_match = serializers.CharField(max_length=128)
    no_of_times = serializers.IntegerField()


class WinnerLocationSerializer(serializers.Serializer):
    venue = serializers.CharField(max_length=128)
    winner = serializers.CharField(max_length=128)
    city = serializers.CharField(max_length=128)
    no_of_times = serializers.IntegerField()


class RunSerializer(serializers.Serializer):
    match_id = serializers.IntegerField(source="id")
    bowler_obj = serializers.SerializerMethodField()

    def get_bowler_obj(self, value):
        deliveries = Delivery.objects.filter(match_id=value["id"])
        bowler_obj = deliveries.values("bowler").annotate(
            runs_given=Sum("total_runs")).order_by("-runs_given").first()

        return bowler_obj

    def to_representation(self, instance):
        value = super().to_representation(instance)
        value["bowler"] = value["bowler_obj"]["bowler"]
        value["runs_given"] = value["bowler_obj"]["runs_given"]
        del value["bowler_obj"]
        return value


class CatchSerializer(serializers.Serializer):
    match_id = serializers.IntegerField(source="id")
    fielder_obj = serializers.SerializerMethodField()

    def get_fielder_obj(self, value):
        deliveries = Delivery.objects.filter(match_id=value["id"])
        fielder_obj = deliveries.values("fielder").annotate(
            catches_taken=Count("dismissal_kind", filter=Q(dismissal_kind="caught"))).order_by("-catches_taken").first()

        return fielder_obj

    def to_representation(self, instance):
        value = super().to_representation(instance)
        value["fielder"] = value["fielder_obj"]["fielder"]
        value["catches_taken"] = value["fielder_obj"]["catches_taken"]
        del value["fielder_obj"]
        return value


class StatSerializer(serializers.Serializer):
    top_winner = WinSerializer()
    winners = serializers.SerializerMethodField()
    toss_winners = serializers.SerializerMethodField()
    toss_and_match_winners = serializers.SerializerMethodField()
    toss_winners_decision = serializers.SerializerMethodField()
    run_winners = serializers.SerializerMethodField()
    wicket_winners = serializers.SerializerMethodField()
    players_of_match = serializers.SerializerMethodField()
    most_win_location = serializers.SerializerMethodField()
    most_runs_given = serializers.SerializerMethodField()
    most_catches_taken = serializers.SerializerMethodField()

    def get_winners(self, value):
        return WinSerializer(value["winners"], many=True).data

    def get_toss_winners(self, value):
        return TossWinSerializer(value["toss_winners"], many=True).data

    def get_toss_and_match_winners(self, value):
        return WinSerializer(value["toss_and_match_winners"], many=True).data

    def get_toss_winners_decision(self, value):
        return TossWinDecisionSerializer(value["toss_winners_decision"], many=True).data

    def get_run_winners(self, value):
        return RunWinSerializer(value["run_winners"], many=True).data

    def get_wicket_winners(self, value):
        return WicketWinSerializer(value["wicket_winners"], many=True).data

    def get_players_of_match(self, value):
        return PlayerOfMatchSerializer(value["players_of_match"], many=True).data

    def get_most_win_location(self, value):
        return WinnerLocationSerializer(value["most_win_location"], many=True).data

    def get_most_runs_given(self, value):
        return RunSerializer(value["most_runs_given"], many=True).data

    def get_most_catches_taken(self, value):
        return CatchSerializer(value["most_catches_taken"], many=True).data
