from rest_framework import serializers
from .models import PartyGroupMessage, PartyGroup


class PartyGroupMessagesSerializer(serializers.ModelSerializer):
    # partyId = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = PartyGroupMessage
        # exclude = ['message_from_user']
        exclude = []

    def create(self, validated_data):
        message = self.Meta.model.objects.create(validated_data, partyGroup_id=validated_data['partyId'])
        return message

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        data = {
            "message_from": instance.message_from,
            "message_from_user": instance.message_from_user.email if instance.message_from_user else None
        }
        representation.update(data)

        return representation


class PartyGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartyGroup
        exclude = []


class WatchPartySerializer(serializers.ModelSerializer):

    # partyId = serializers.CharField(max_length=128, read_only=True)
    class Meta:
        model = PartyGroup
        exclude = []
