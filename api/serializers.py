from rest_framework import serializers

class StateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    state = serializers.ChoiceField(choices=["flow", "stressed", "disengaged", "sensor issues"])