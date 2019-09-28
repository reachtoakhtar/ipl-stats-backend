import logging
from django.urls import path

from ipl_stat.views import LookupCreateView, StatsView

__author__ = "akhtar"

logger = logging.getLogger(__name__)


urlpatterns = [
    path('lookups/', LookupCreateView.as_view(), name="lookups"),
    path('stats/', StatsView.as_view(), name="stats"),
]
