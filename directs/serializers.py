from rest_framework import serializers
from .models import ManufacturerMessage, ClientMessage


class ClientMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMessage
        fields = '__all__'


class ManufacturerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerMessage
        fields = '__all__'