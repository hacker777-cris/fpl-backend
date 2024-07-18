from django.urls import path
from . import views

urlpatterns = [
    path("matches/", views.MatchView.as_view()),
    path("team-fixtures/", views.TeamFixturesView.as_view()),
    path("update-fixtures/", views.UpdateFixturesView.as_view()),
    path("update-data/", views.UpdateDataView.as_view()),
    path("player-by-position/", views.PlayersByPositionAPIView.as_view()),
]
