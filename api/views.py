import requests
from rest_framework import views, response, status
from rest_framework.response import Response
from django.conf import settings
from collections import defaultdict
from dotenv import load_dotenv
import os
from datetime import datetime

from rest_framework.utils.representation import serializer_repr
from .models import Fixture
from .models import Team, Player, PlayerPosition, GameweekStats
from .serializers import (
    PlayerSerializer,
    TeamSerializer,
    SingularTeamSerializer,
    PlayerListSerializer,
)  # Assuming you have a serializer
import logging

logger = logging.getLogger(__name__)

load_dotenv()


class MatchView(views.APIView):
    def get(self, request):
        auth_key = os.getenv("OUTLET_AUTH_KEY")
        referer = os.getenv("REFERER")
        url = f"http://api.performfeeds.com/soccerdata/match/{auth_key}"
        params = {
            "live": "yes",
            "_fmt": "json",
            "tmcl": "9n12waklv005j8r32sfjj2eqc",
            "_rt": "c",
            "_lcl": "en-op",
            "_pgSz": 400,
        }
        headers = {"Referer": referer}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()  # Raise an exception if the request failed
            data = res.json()

            matches_by_date = defaultdict(list)
            for match in data["match"]:
                match_info = match["matchInfo"]
                contestants = match_info["contestant"]
                venue = match_info["venue"]

                matches_by_date[match_info["date"]].append(
                    {
                        "localTime": match_info["localTime"],
                        "teams": [
                            {"id": contestant["id"], "name": contestant["name"]}
                            for contestant in contestants
                        ],
                        "venue": venue["longName"],
                    }
                )
                # Sort the matches by date in ascending order
            sorted_matches_by_date = dict(
                sorted(
                    matches_by_date.items(),
                    key=lambda item: datetime.strptime(item[0], "%Y-%m-%dZ"),
                )
            )
            return response.Response(
                {"success": True, "matches": sorted_matches_by_date},
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TeamFixturesView(views.APIView):
    def get(self, request):
        team_id = request.query_params.get("team_id")
        print("This is team_id", team_id)
        if not team_id:
            return response.Response(
                {"error": "team_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        auth_key = os.getenv("OUTLET_AUTH_KEY")
        referer = os.getenv("REFERER")
        url = f"http://api.performfeeds.com/soccerdata/match/{auth_key}"
        params = {
            "live": "yes",
            "_fmt": "json",
            "tmcl": "9n12waklv005j8r32sfjj2eqc",
            "_rt": "c",
            "_lcl": "en-op",
            "_pgSz": 400,
            "ctst": team_id,
        }
        headers = {"Referer": referer}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()  # Raise an exception if the request failed
            data = res.json()

            matches_by_date = defaultdict(list)
            for match in data["match"]:
                match_info = match["matchInfo"]
                contestants = match_info["contestant"]
                venue = match_info["venue"]

                matches_by_date[match_info["date"]].append(
                    {
                        "localTime": match_info["localTime"],
                        "teams": [
                            {"id": contestant["id"], "name": contestant["name"]}
                            for contestant in contestants
                        ],
                        "venue": venue["longName"],
                    }
                )
                # Sort the matches by date in ascending order
            sorted_matches_by_date = dict(
                sorted(
                    matches_by_date.items(),
                    key=lambda item: datetime.strptime(item[0], "%Y-%m-%dZ"),
                )
            )

            return response.Response(
                {"success": True, "matches": sorted_matches_by_date},
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateFixturesView(views.APIView):
    def get(self, request):
        auth_key = os.getenv("OUTLET_AUTH_KEY")
        referer = os.getenv("REFERER")
        url = f"http://api.performfeeds.com/soccerdata/match/{auth_key}"
        params = {
            "live": "yes",
            "_fmt": "json",
            "tmcl": "9n12waklv005j8r32sfjj2eqc",
            "_rt": "c",
            "_lcl": "en-op",
            "_pgSz": 400,
        }
        headers = {"Referer": referer}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()  # Raise an exception if the request failed
            data = res.json()

            updated_fixtures = 0
            for match in data["match"]:
                match_info = match["matchInfo"]
                contestants = match_info["contestant"]
                venue = match_info["venue"]

                # Extract the necessary information from the match object
                date = datetime.strptime(match_info["date"], "%Y-%m-%dZ").date()
                home_team = contestants[0]["name"]
                away_team = contestants[1]["name"]
                stadium = venue["longName"]
                time = datetime.strptime(match_info["localTime"], "%H:%M:%S").time()
                competition_name = match_info["competition"]["name"]
                week = int(match_info["week"])

                # Create or update the fixture object in the database
                fixture, created = Fixture.objects.update_or_create(
                    date=date,
                    home_team=home_team,
                    away_team=away_team,
                    defaults={
                        "stadium": stadium,
                        "time": time,
                        "competition_name": competition_name,
                        "week": week,
                    },
                )

                if created:
                    updated_fixtures += 1

            return response.Response(
                {"success": True, "updated_fixtures": updated_fixtures},
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateDataView(views.APIView):
    def get(self, request):
        url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        response_data = requests.get(url).json()

        # Update teams
        teams_data = response_data["teams"]
        for team_data in teams_data:
            defaults = {
                "code": team_data["code"],
                "draw": team_data["draw"],
                "form": team_data["form"],
                "loss": team_data["loss"],
                "name": team_data["name"],
                "played": team_data["played"],
                "points": team_data["points"],
                "position": team_data["position"],
                "short_name": team_data["short_name"],
                "strength": team_data["strength"],
                "team_division": team_data["team_division"],
                "unavailable": team_data["unavailable"],
                "win": team_data["win"],
                "strength_overall_home": team_data["strength_overall_home"],
                "strength_overall_away": team_data["strength_overall_away"],
                "strength_attack_home": team_data["strength_attack_home"],
                "strength_attack_away": team_data["strength_attack_away"],
                "strength_defence_home": team_data["strength_defence_home"],
                "strength_defence_away": team_data["strength_defence_away"],
                "pulse_id": team_data["pulse_id"],
            }
            Team.objects.update_or_create(id=team_data["id"], defaults=defaults)

        # Update player positions
        player_positions_data = response_data["element_types"]
        for player_position_data in player_positions_data:
            defaults = {
                "plural_name": player_position_data["plural_name"],
                "plural_name_short": player_position_data["plural_name_short"],
                "singular_name": player_position_data["singular_name"],
                "singular_name_short": player_position_data["singular_name_short"],
                "squad_select": player_position_data["squad_select"],
                "squad_min_select": player_position_data.get("squad_min_select"),
                "squad_max_select": player_position_data.get("squad_max_select"),
                "squad_min_play": player_position_data["squad_min_play"],
                "squad_max_play": player_position_data["squad_max_play"],
                "ui_shirt_specific": player_position_data["ui_shirt_specific"],
                "sub_positions_locked": player_position_data["sub_positions_locked"],
                "element_count": player_position_data["element_count"],
            }
            PlayerPosition.objects.update_or_create(
                id=player_position_data["id"], defaults=defaults
            )

        # Update players
        players_data = response_data["elements"]
        for player_data in players_data:
            defaults = {
                "chance_of_playing_next_round": player_data[
                    "chance_of_playing_next_round"
                ],
                "chance_of_playing_this_round": player_data[
                    "chance_of_playing_this_round"
                ],
                "code": player_data["code"],
                "cost_change_event": player_data["cost_change_event"],
                "cost_change_event_fall": player_data["cost_change_event_fall"],
                "cost_change_start": player_data["cost_change_start"],
                "cost_change_start_fall": player_data["cost_change_start_fall"],
                "dreamteam_count": player_data["dreamteam_count"],
                "element_type": player_data["element_type"],
                "ep_next": player_data["ep_next"],
                "ep_this": player_data["ep_this"],
                "event_points": player_data["event_points"],
                "first_name": player_data["first_name"],
                "form": player_data["form"],
                "in_dreamteam": player_data["in_dreamteam"],
                "news": player_data["news"],
                "news_added": player_data["news_added"],
                "now_cost": player_data["now_cost"],
                "photo": player_data["photo"],
                "points_per_game": player_data["points_per_game"],
                "second_name": player_data["second_name"],
                "selected_by_percent": player_data["selected_by_percent"],
                "special": player_data["special"],
                "squad_number": player_data.get("squad_number"),
                "status": player_data["status"],
                "team": player_data["team"],
                "team_code": player_data["team_code"],
                "total_points": player_data["total_points"],
                "transfers_in": player_data["transfers_in"],
                "transfers_in_event": player_data["transfers_in_event"],
                "transfers_out": player_data["transfers_out"],
                "transfers_out_event": player_data["transfers_out_event"],
                "value_form": player_data["value_form"],
                "value_season": player_data["value_season"],
                "web_name": player_data["web_name"],
                "minutes": player_data["minutes"],
                "goals_scored": player_data["goals_scored"],
                "assists": player_data["assists"],
                "clean_sheets": player_data["clean_sheets"],
                "goals_conceded": player_data["goals_conceded"],
                "own_goals": player_data["own_goals"],
                "penalties_saved": player_data["penalties_saved"],
                "penalties_missed": player_data["penalties_missed"],
                "yellow_cards": player_data["yellow_cards"],
                "red_cards": player_data["red_cards"],
                "saves": player_data["saves"],
                "bonus": player_data["bonus"],
                "bps": player_data["bps"],
                "influence": player_data["influence"],
                "creativity": player_data["creativity"],
                "threat": player_data["threat"],
                "ict_index": player_data["ict_index"],
                "starts": player_data["starts"],
                "expected_goals": player_data["expected_goals"],
                "expected_assists": player_data["expected_assists"],
                "expected_goal_involvements": player_data["expected_goal_involvements"],
                "expected_goals_conceded": player_data["expected_goals_conceded"],
                "influence_rank": player_data["influence_rank"],
                "influence_rank_type": player_data["influence_rank_type"],
                "creativity_rank": player_data["creativity_rank"],
                "creativity_rank_type": player_data["creativity_rank_type"],
                "threat_rank": player_data["threat_rank"],
                "threat_rank_type": player_data["threat_rank_type"],
                "ict_index_rank": player_data["ict_index_rank"],
                "ict_index_rank_type": player_data["ict_index_rank_type"],
                "corners_and_indirect_freekicks_order": player_data.get(
                    "corners_and_indirect_freekicks_order"
                ),
                "corners_and_indirect_freekicks_text": player_data[
                    "corners_and_indirect_freekicks_text"
                ],
                "direct_freekicks_order": player_data.get("direct_freekicks_order"),
                "direct_freekicks_text": player_data["direct_freekicks_text"],
                "penalties_order": player_data.get("penalties_order"),
                "penalties_text": player_data["penalties_text"],
                "expected_goals_per_90": player_data["expected_goals_per_90"],
                "saves_per_90": player_data["saves_per_90"],
                "expected_assists_per_90": player_data["expected_assists_per_90"],
                "expected_goal_involvements_per_90": player_data[
                    "expected_goal_involvements_per_90"
                ],
                "expected_goals_conceded_per_90": player_data[
                    "expected_goals_conceded_per_90"
                ],
                "goals_conceded_per_90": player_data["goals_conceded_per_90"],
                "now_cost_rank": player_data["now_cost_rank"],
                "now_cost_rank_type": player_data["now_cost_rank_type"],
                "form_rank": player_data["form_rank"],
                "form_rank_type": player_data["form_rank_type"],
                "points_per_game_rank": player_data["points_per_game_rank"],
                "points_per_game_rank_type": player_data["points_per_game_rank_type"],
                "selected_rank": player_data["selected_rank"],
                "selected_rank_type": player_data["selected_rank_type"],
                "starts_per_90": player_data["starts_per_90"],
                "clean_sheets_per_90": player_data["clean_sheets_per_90"],
            }
            Player.objects.update_or_create(id=player_data["id"], defaults=defaults)

        # Update gameweek stats
        gameweek_stats_data = response_data["events"]
        for gameweek_data in gameweek_stats_data:
            defaults = {
                "name": gameweek_data["name"],
                "deadline_time": gameweek_data["deadline_time"],
                "release_time": gameweek_data.get("release_time"),
                "average_entry_score": gameweek_data["average_entry_score"],
                "finished": gameweek_data["finished"],
                "data_checked": gameweek_data["data_checked"],
                "highest_scoring_entry": gameweek_data.get("highest_scoring_entry"),
                "deadline_time_epoch": gameweek_data["deadline_time_epoch"],
                "deadline_time_game_offset": gameweek_data["deadline_time_game_offset"],
                "highest_score": gameweek_data.get("highest_score"),
                "is_previous": gameweek_data["is_previous"],
                "is_current": gameweek_data["is_current"],
                "is_next": gameweek_data["is_next"],
                "cup_leagues_created": gameweek_data["cup_leagues_created"],
                "h2h_ko_matches_created": gameweek_data["h2h_ko_matches_created"],
                "ranked_count": gameweek_data["ranked_count"],
                "transfers_made": gameweek_data["transfers_made"],
                "most_selected": gameweek_data["most_selected"],
                "most_transferred_in": gameweek_data["most_transferred_in"],
                "top_element": gameweek_data["top_element"],
                "top_element_info": gameweek_data.get("top_element_info"),
                "most_captained": gameweek_data["most_captained"],
                "most_vice_captained": gameweek_data["most_vice_captained"],
            }
            GameweekStats.objects.update_or_create(
                id=gameweek_data["id"], defaults=defaults
            )

        return response.Response(
            {"message": "Data updated successfully"}, status=status.HTTP_200_OK
        )


class PlayersByPositionAPIView(views.APIView):
    def get(self, request):
        element_type = request.query_params.get("element_type")

        if not element_type:
            return Response(
                {"error": "element_type query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            players = Player.objects.filter(element_type=element_type)
            serializer = PlayerSerializer(
                players, many=True
            )  # Replace with your serializer
            data = serializer.data
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response(
                {"error": "Players not found for the given element_type"},
                status=status.HTTP_404_NOT_FOUND,
            )


class TeamListAPIView(views.APIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamDetailAPIView(views.APIView):
    def get(self, request):
        team_id = request.query_params.get("team_id")
        if not team_id:
            return Response(
                {"error": "Team id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SingularTeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamPlayersAPIView(views.APIView):
    def get(self, request):
        team_id = request.query_params.get("team_id")
        if not team_id:
            return Response(
                {"error": "Team id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        players = Player.objects.filter(team=team_id)
        serializer = PlayerListSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerDetailView(views.APIView):
    def get(self, request):
        player_id = request.query_params.get("player_id")

        if not player_id:
            return Response(
                {"error": "Player ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response(
                {"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the player data
        player_serializer = PlayerSerializer(player)
        player_data = player_serializer.data

        # Fetch player fixtures
        fixtures_url = (
            f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        )
        try:
            fixtures_response = requests.get(fixtures_url)
            fixtures_response.raise_for_status()
            fixtures_data = fixtures_response.json()
        except requests.RequestException as e:
            return Response(
                {"error": f"Failed to fetch player fixtures: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Extract player team and fixture information
        player_team_id = player_data.get("team")
        fixtures = fixtures_data.get("fixtures", [])
        fixture_info = []

        # Create a mapping of team IDs to team short names
        teams = Team.objects.all()
        team_mapping = {team.id: team.short_name for team in teams}

        for fixture in fixtures:
            is_home = fixture.get("team_h") == player_team_id
            opponent_team_id = (
                fixture.get("team_a") if is_home else fixture.get("team_h")
            )
            fixture_type = "home" if is_home else "away"

            if opponent_team_id:
                fixture_info.append(
                    {
                        "event_name": fixture.get("event_name"),
                        "opponent_team": team_mapping.get(opponent_team_id, "Unknown"),
                        "difficulty": fixture.get("difficulty"),
                        "fixture_type": fixture_type,
                    }
                )

        # Combine player data with filtered fixture info
        player_data["fixtures"] = fixture_info

        return Response(player_data, status=status.HTTP_200_OK)


class GetAllPlayers(views.APIView):
    def get(self, request):
        try:
            players = Player.objects.all()
            serializer = PlayerSerializer(players, many=True)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except Player.DoesNotExist:
            logger.error("Players not found")
            return Response(
                {"success": False, "error": "Players not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response(
                {"success": False, "error": "An error occurred while fetching players"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
