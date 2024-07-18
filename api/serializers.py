from rest_framework import serializers
from .models import Team, PlayerPosition, Player, GameweekStats


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class PlayerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPosition
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"  # Serialize all fields of the Player model


class GameweekStatsSerializer(serializers.ModelSerializer):
    most_selected = PlayerSerializer()
    most_transferred_in = PlayerSerializer()
    top_element = PlayerSerializer()
    most_captained = PlayerSerializer()
    most_vice_captained = PlayerSerializer()

    class Meta:
        model = GameweekStats
        fields = "__all__"

    def create(self, validated_data):
        most_selected_data = validated_data.pop("most_selected")
        most_selected, _ = Player.objects.get_or_create(**most_selected_data)
        most_transferred_in_data = validated_data.pop("most_transferred_in")
        most_transferred_in, _ = Player.objects.get_or_create(
            **most_transferred_in_data
        )
        top_element_data = validated_data.pop("top_element")
        top_element, _ = Player.objects.get_or_create(**top_element_data)
        most_captained_data = validated_data.pop("most_captained")
        most_captained, _ = Player.objects.get_or_create(**most_captained_data)
        most_vice_captained_data = validated_data.pop("most_vice_captained")
        most_vice_captained, _ = Player.objects.get_or_create(
            **most_vice_captained_data
        )
        gameweek_stats = GameweekStats.objects.create(
            most_selected=most_selected,
            most_transferred_in=most_transferred_in,
            top_element=top_element,
            most_captained=most_captained,
            most_vice_captained=most_vice_captained,
            **validated_data,
        )
        return gameweek_stats

    def update(self, instance, validated_data):
        most_selected_data = validated_data.pop("most_selected")
        most_selected, _ = Player.objects.get_or_create(**most_selected_data)
        instance.most_selected = most_selected

        most_transferred_in_data = validated_data.pop("most_transferred_in")
        most_transferred_in, _ = Player.objects.get_or_create(
            **most_transferred_in_data
        )
        instance.most_transferred_in = most_transferred_in

        top_element_data = validated_data.pop("top_element")
        top_element, _ = Player.objects.get_or_create(**top_element_data)
        instance.top_element = top_element

        most_captained_data = validated_data.pop("most_captained")
        most_captained, _ = Player.objects.get_or_create(**most_captained_data)
        instance.most_captained = most_captained

        most_vice_captained_data = validated_data.pop("most_vice_captained")
        most_vice_captained, _ = Player.objects.get_or_create(
            **most_vice_captained_data
        )
        instance.most_vice_captained = most_vice_captained

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
