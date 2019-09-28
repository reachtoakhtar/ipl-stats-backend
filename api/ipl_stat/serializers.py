import logging

from rest_framework import serializers

__author__ = "akhtar"

logger = logging.getLogger(__name__)


class WinSerializer(serializers.Serializer):
    winner = serializers.CharField(max_length=128)
    no_of_wins = serializers.IntegerField()


class TossWinSerializer(serializers.Serializer):
    toss_winner = serializers.CharField(max_length=128)
    no_of_wins = serializers.IntegerField()


class PlayerOfMatchSerializer(serializers.Serializer):
    player_of_match = serializers.CharField(max_length=128)
    no_of_times = serializers.IntegerField()


class WinnerLocationSerializer(serializers.Serializer):
    venue = serializers.CharField(max_length=128)
    winner = serializers.CharField(max_length=128)
    no_of_times = serializers.IntegerField()


class StatSerializer(serializers.Serializer):
    winners = serializers.SerializerMethodField()
    toss_winners = serializers.SerializerMethodField()
    players_of_match = serializers.SerializerMethodField()
    most_win_location = serializers.SerializerMethodField()
    top_winner = WinSerializer()

    def get_winners(self, value):
        return WinSerializer(value["winners"], many=True).data

    def get_toss_winners(self, value):
        return TossWinSerializer(value["toss_winners"], many=True).data

    def get_players_of_match(self, value):
        return PlayerOfMatchSerializer(value["players_of_match"], many=True).data

    def get_most_win_location(self, value):
        return WinnerLocationSerializer(value["most_win_location"], many=True).data
