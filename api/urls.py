from django.urls import path
from . import views

urlpatterns = [
    path("matches/", views.MatchView.as_view()),
    path("team-fixtures/", views.TeamFixturesView.as_view()),
    path("update-fixtures/", views.UpdateFixturesView.as_view()),
    path("update-data/", views.UpdateDataView.as_view()),
    path("player-by-position/", views.PlayersByPositionAPIView.as_view()),
    path("get-teams/", views.TeamListAPIView.as_view()),
    path("get-single-team/", views.TeamDetailAPIView.as_view()),
    path("team-players/", views.TeamPlayersAPIView.as_view(), name="team-players"),
    path("player/", views.PlayerDetailView.as_view(), name="player-detail"),
    path("all-players/", views.GetAllPlayers.as_view(), name="all-players"),
]
