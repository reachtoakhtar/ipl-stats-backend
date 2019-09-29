import os

import pandas as pd
from django.db.models import Count, Max, Q, F
from rest_framework import status

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from ipl_stat.models import Delivery, Match
from ipl_stat.serializers import StatSerializer


class LookupCreateView(CreateAPIView):
    @staticmethod
    def get_object_list(csv_file_name, model_class):
        object_list = []
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures", csv_file_name)
        df = pd.read_csv(path)
        df = df.where((pd.notnull(df)), None)
        headers = list(df.columns)
        for row in df.iterrows():
            row = row[1].tolist()
            kwargs = dict(zip(headers, row))
            object = model_class(**kwargs)
            object_list.append(object)

        return object_list

    def create(self, request, request_data=None, *args, **kwargs):
        match_object_list = LookupCreateView.get_object_list("matches.csv", Match)
        delivery_object_list = LookupCreateView.get_object_list("deliveries.csv", Delivery)

        Match.objects.bulk_create(match_object_list)
        Delivery.objects.bulk_create(delivery_object_list)

        return Response(data={"message": "Applied fixtures successfully."}, status=status.HTTP_200_OK)


class StatsView(ListAPIView):
    serializer_class = StatSerializer

    def get_queryset(self):
        season = int(self.request.query_params.get("season"))
        return Match.objects.filter(season=season)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        winners = queryset.values("winner").annotate(
            no_of_wins=Count("winner")).order_by("-no_of_wins")

        toss_winners = queryset.values("toss_winner").annotate(
            no_of_wins=Count("toss_winner")).order_by("-no_of_wins")

        toss_winners_decision = queryset.values("toss_winner").annotate(
            no_of_wins=Count("toss_winner"),
            field_times=Count("toss_decision", filter=Q(toss_decision="field")),
            bat_times=Count("toss_decision", filter=Q(toss_decision="bat"))
        )

        run_winners = queryset.values("winner").annotate(
            max_win_margin=Max("win_by_runs")).order_by("-max_win_margin")

        wicket_winners = queryset.values("winner").annotate(
            max_win_wickets=Max("win_by_wickets")).order_by("-max_win_wickets")

        toss_and_match_winners = queryset.values("winner").annotate(
            no_of_wins=Count("winner", filter=Q(toss_winner=F("winner")))).order_by("-no_of_wins")

        players_of_match = queryset.values("player_of_match").annotate(
            no_of_times=Count("player_of_match")).order_by("-no_of_times")

        most_win_location = queryset.values("venue", "winner", "city").filter(
            winner=winners[0]["winner"]).annotate(
            no_of_times=Count("venue")).order_by("-no_of_times")

        serializer_data = {
            "winners": winners,
            "top_winner": winners[0],
            "toss_winners": toss_winners,
            "toss_and_match_winners": toss_and_match_winners,
            "toss_winners_decision": toss_winners_decision,
            "run_winners": run_winners,
            "wicket_winners": wicket_winners,
            "players_of_match": players_of_match,
            "most_win_location": most_win_location,
            "most_runs_given": queryset.values("id"),
            "most_catches_taken": queryset.values("id")
        }
        data = self.serializer_class(serializer_data).data
        return Response(data=data, status=status.HTTP_200_OK)
